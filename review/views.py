from django.shortcuts import render,redirect
from django.views import View

from django.db.models import Q

from .models import Movie,Comment
from .forms import CommentForm


class IndexView(View):

    def get(self, request, *args, **kwargs):

        comments = Comment.objects.filter(target=2)
        print(comments)

        if "search" in request.GET:
            #TODO:ここで検索処理を実行
            print(request.GET["search"])

            #(1)キーワードが空欄もしくはスペースのみの場合、トップページにリダイレクト
            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("review:index")

            #『バイオハザード 主演』["バイオハザード","主演"]
            search = request.GET["search"].replace("　"," ")
            search_list = search.split(" ")

            query       = Q()
            for word in search_list:
                # 空欄の場合は次のループへ
                if word == "":
                    continue

                # TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query &= Q(title__contains=word)

            movies = Movie.objects.filter(query).order_by("-dt")
        else:
            movies = Movie.objects.all().order_by("-dt")


        context = { "movies":movies }

        return render(request,"review/index.html",context)

index   = IndexView.as_view()

class SingleView(View):
    def get(self, request, pk, *args, **kwargs):

        #ここで必要なデータを検索している
        movie       = Movie.objects.filter(id=pk).first()
        comments    = Comment.objects.filter(target=pk).order_by("-dt")

        if not movie:
            return redirect("review:index")

        context = { "movie":movie,
                    "comments":comments
                    }

        return render(request,"review/single.html",context)

    def post(self, request, pk, *args, **kwargs):

        #TODO:ここでpkをセットする
        copied              = request.POST.copy()
        copied["target"]    = pk
        form                = CommentForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("review:single",pk)

single   = SingleView.as_view()
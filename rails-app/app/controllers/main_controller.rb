class MainController < ApplicationController

    def index
        if params["article"]
            @article = Article.find(params["article"])
        else
            @article = nil
        end
        if params["result"] == "added"
            @added = true
        else
            @added = false
        end
    end

    def action
        if params['read']
            article = addArticleForUser(params['url'], current_user)         
            redirect_to root_url(:article => article.id)
        else
            addArticleForUser(params['url'], current_user)
            redirect_to root_url(:result => "added")
        end  
    end

    private

    def addArticleForUser(url, user)
        article = Article.find_by_url(url)
        if article == nil
            cmd = "python3 app/scripts/get_article.py %s" % Shellwords.escape(url)
            out, err, st = Open3.capture3(cmd)
            artjson = JSON.parse(out)
            article = Article.new()
            article[:title] = artjson["title"]
            article[:text] = artjson["text"]
            article[:url] = url
            article[:authors] = JSON.dump(artjson["authors"])
            article.save
        end
        if UserArticle.where(user: user, article: article).length == 0
            UserArticle.create(user: user, article: article)
        end
        return article
    end


end

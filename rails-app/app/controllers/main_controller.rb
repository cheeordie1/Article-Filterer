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
            url = params['url']
            cmd = "python3 app/scripts/get_article.py %s" % Shellwords.escape(url)
            out, err, st = Open3.capture3(cmd)
            artjson = JSON.parse(out)
            article = Article.new()
            article[:title] = artjson["title"]
            article[:text] = artjson["text"]
            article[:url] = url
            article.save
            UserArticle.create(:user => current_user, :article => article)
            redirect_to root_url(:article => article.id)
        else
            url = params['url']
            cmd = "python3 app/scripts/get_article.py %s" % Shellwords.escape(url)
            out, err, st = Open3.capture3(cmd)
            artjson = JSON.parse(out)
            article = Article.new()
            article[:title] = artjson["title"]
            article[:text] = artjson["text"]
            article[:url] = url
            article.save
            UserArticle.create(:user => current_user, :article => article)
            redirect_to root_url(:result => "added")
        end  
    end
end

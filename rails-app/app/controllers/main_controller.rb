require 'net/http'

class MainController < ApplicationController

    def index
        if params["article"]
            @article = Article.find(params["article"])
            @highlighted = highlightArticle(@article, current_user)
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

    def highlightArticle(article, user)
        http = Net::HTTP.new('nlp', 5001)
        request = Net::HTTP::Post.new('/highlight', {'Content-Type' => 'application/json'})
        data = {article_id: article.id, user_id: user.id}
        request.body = data.to_json
        response = http.request(request)
        highlighted = JSON.parse(response.body())
        return highlighted
    end

    def addArticleForUser(url, user)
        article = Article.find_by_url(url)
        if article == nil
            data = {url: url}
            http = Net::HTTP.new('scraper', 5000)
            request = Net::HTTP::Post.new('/get_article', {'Content-Type' => 'application/json'})
            request.body = data.to_json
            response = http.request(request)
            # cmd = "python3 app/scripts/get_article.py %s" % Shellwords.escape(url)
            # out, err, st = Open3.capture3(cmd)
            puts response.body()
            artjson = JSON.parse(response.body())
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

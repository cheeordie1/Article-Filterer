require 'net/http'

class MainController < ApplicationController

    def index
        if params["article"]
            @article = Article.find(params["article"])
            p 'Article Id = '
            p @article.id
            if params['readbefore'] and params['readbefore'] == 'true'
                @readbefore = true
            else
                @readbefore = false
            end
        else
            @article = nil
        end
        if params["result"]
            @result = params["result"]
        else
            @result = ''
        end

        # if params["result"] == "added"
        #     @added = true
        # else
        #     @added = false
        # end
    end

    def action
        if params['read']
            params['url'] = params['url'].strip
            article, readbefore = addArticleForUser(params['url'], current_user)   
            if article == 'error'
                redirect_to root_url(:result => 'error')  
            else    
                redirect_to root_url(:article => article.id, :readbefore => readbefore)
            end
        else
          result = "added"
          if params['formType'] == "text"
            params['url'] = params['url'].strip
            addArticleForUser(params['url'], current_user)
          else
            file_data = params['file']
            if file_data.respond_to?(:read)
              xml_contents = file_data.read
            elsif file_data.respond_to?(:path)
              xml_contents = File.read(file_data)
            else
              logger.error "Bad file_data: #{file_data.class.name}: #{file_data.inspect}"
              result = "error"
            end
            if result != "error"
              xml_contents.each_line do |url|
                addArticleForUser(url, current_user)
              end
            end
          end
          redirect_to root_url(:result => result)
        end  
    end

    def clear
      UserArticle.where(user: current_user).destroy_all
      redirect_to root_url
    end


    private

    def addArticleForUser(url, user)
        article = Article.find_by_url(url)
        if article == nil
            data = {url: url}
            http = Net::HTTP.new('scraper', 5000)
            request = Net::HTTP::Post.new('/get_article', {'Content-Type' => 'application/json'})
            request.body = data.to_json
            response = http.request(request)
            p 'response from parser'
            p response
            # cmd = "python3 app/scripts/get_article.py %s" % Shellwords.escape(url)
            # out, err, st = Open3.capture3(cmd)
            artjson = JSON.parse(response.body())
            article = Article.new()
            if artjson['text'] == nil
                return 'error'
            end
            article[:title] = artjson["title"]
            article[:text] = artjson["text"]
            article[:url] = url
            article[:authors] = artjson["authors"]
            article.save
        end
        if UserArticle.where(user: user, article: article).length == 0
            UserArticle.create(user: user, article: article)
        else
            return article, true
        end
        return article, false
    end


end

class MainController < ApplicationController

    def index
        if params["article"]
            @article = Article.find(params["article"])
            puts "size is " << @article.getParagraphs().size.to_s()
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
          result = "added"
          if params['formType'] == "text"
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
          redirect_to root_url(:result => result)
        end  
    end

    private

    def addArticleForUser(url, user)
        article = Article.find_by_url(url)
        if article == nil
            cmd = "python app/scripts/get_article.py %s" % Shellwords.escape(url)
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

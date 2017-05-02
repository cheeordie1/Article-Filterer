class MainController < ApplicationController

    def index

    end

    def action
        if params['read']
            puts 'read'
        else
            puts 'add'
        end
        redirect_to root_path
    end
end

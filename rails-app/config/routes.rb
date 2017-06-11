Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  get '/auth/:provider/callback', to: 'sessions#create'
  delete '/logout', to: 'sessions#destroy'
  post '/action', to: "main#action"
  root to: 'main#index'
  get '/clear', to: 'main#clear'
end

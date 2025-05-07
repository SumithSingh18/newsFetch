from flask import Flask, request
import requests
app = Flask(__name__)

# Replace this with your actual News API key
NEWS_API_KEY = "3872ca0dfc7f4fe49d5cc0bdc4362ca8"

@app.route('/')
def index():
    # Get category from URL parameter, default to "general"
    category = request.args.get('category', 'general')
    
    # Fetch news from News API
    url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        news_data = response.json()
        
        # Build the HTML response
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>News Headlines</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                h1 {{
                    color: #333;
                    text-transform: capitalize;
                }}
                .news-item {{
                    background-color: white;
                    margin-bottom: 20px;
                    padding: 15px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .news-title {{
                    margin-top: 0;
                    color: #2c3e50;
                }}
                .news-description {{
                    color: #555;
                }}
                .news-meta {{
                    color: #888;
                    font-size: 0.9em;
                    margin-top: 10px;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .categories {{
                    margin-bottom: 20px;
                }}
                .categories a {{
                    display: inline-block;
                    margin-right: 10px;
                    padding: 5px 10px;
                    background-color: #3498db;
                    color: white;
                    border-radius: 3px;
                }}
                .categories a:hover {{
                    background-color: #2980b9;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <h1>{category} News</h1>
            
            <div class="categories">
                <a href="/?category=general">Generally</a>
                <a href="/?category=business">Business</a>
                <a href="/?category=technology">Technology</a>
                <a href="/?category=sports">Sports</a>
                <a href="/?category=entertainment">Entertainment</a>
                <a href="/?category=health">Health</a>
                <a href="/?category=science">Science</a>
            </div>
        '''
        
        # Check if we got articles
        if news_data.get('status') == 'ok' and news_data.get('articles'):
            for article in news_data['articles']:
                html += f'''
                <div class="news-item">
                    <h2 class="news-title">
                        <a href="{article.get('url', '#')}" target="_blank">
                            {article.get('title', 'No Title')}
                        </a>
                    </h2>
                    <p class="news-description">{article.get('description', 'No description available.')}</p>
                    <div class="news-meta">
                        Source: {article.get('source', {}).get('name', 'Unknown')} | 
                        Published: {article.get('publishedAt', 'Unknown')}
                    </div>
                </div>
                '''
        else:
            html += '<p>No news articles found or API error occurred.</p>'
            if news_data.get('message'):
                html += f'<p>Error message: {news_data.get("message")}</p>'
        
        html += '''
        </body>
        </html>
        '''
        
        return html
        
    except Exception as e:
        return f'''
        <html>
            <body>
                <h1>Error</h1>
                <p>Failed to fetch news: {str(e)}</p>
                <p>Make sure you have replaced "YOUR_API_KEY_HERE" with your actual News API key.</p>
            </body>
        </html>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import openai
import google.generativeai as genai
import anthropic
import os
import json
import time
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Use env var or fallback
CORS(app)

# Optional: Pre-configure APIs from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookGenerator:
    def __init__(self):
        self.openai_client = None
        self.genai_model = None
        self.anthropic_client = None
    
    def configure_apis(self, api_configs):
        """Configure API clients based on provided configurations"""
        try:
            if api_configs.get('openai_key'):
                openai.api_key = api_configs['openai_key']
                self.openai_client = openai.OpenAI(api_key=api_configs['openai_key'])
                logger.info("OpenAI configured successfully")
            
            if api_configs.get('gemini_key'):
                genai.configure(api_key=api_configs['gemini_key'])
                self.genai_model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini configured successfully")
            
            if api_configs.get('anthropic_key'):
                self.anthropic_client = anthropic.Anthropic(api_key=api_configs['anthropic_key'])
                logger.info("Anthropic configured successfully")
            
            return True
        except Exception as e:
            logger.error(f"Error configuring APIs: {str(e)}")
            return False
    
    def generate_with_openai(self, prompt, max_tokens=4000):
        """Generate content using OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional book writer. Create engaging, well-structured content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e
    
    def generate_with_gemini(self, prompt):
        """Generate content using Gemini API"""
        try:
            response = self.genai_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise e
    
    def generate_with_anthropic(self, prompt, max_tokens=4000):
        """Generate content using Anthropic API"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=max_tokens,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise e
    
    def generate_content(self, provider, prompt, max_tokens=4000):
        """Generate content using specified provider"""
        if provider == 'openai':
            return self.generate_with_openai(prompt, max_tokens)
        elif provider == 'gemini':
            return self.generate_with_gemini(prompt)
        elif provider == 'anthropic':
            return self.generate_with_anthropic(prompt, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def create_book_outline(self, provider, book_data):
        """Create a detailed book outline"""
        prompt = f"""
        Create a detailed book outline for a {book_data['genre']} book with the following specifications:
        
        Title: {book_data['title']}
        Target Audience: {book_data['target_audience']}
        Main Theme: {book_data['theme']}
        Estimated Length: {book_data['length']} words
        
        Additional Details:
        {book_data.get('additional_details', '')}
        
        Please provide:
        1. A compelling book summary
        2. Detailed chapter outline (aim for {book_data.get('num_chapters', 10)} chapters)
        3. Character descriptions (if applicable)
        4. Key plot points or main concepts
        5. Tone and style recommendations
        
        Format the response clearly with headers for each section.
        """
        
        return self.generate_content(provider, prompt)
    
    def generate_chapter(self, provider, book_data, chapter_info, outline):
        """Generate a single chapter"""
        prompt = f"""
        Write Chapter {chapter_info['number']}: "{chapter_info['title']}" for the book "{book_data['title']}".
        
        Book Context:
        - Genre: {book_data['genre']}
        - Target Audience: {book_data['target_audience']}
        - Theme: {book_data['theme']}
        
        Chapter Guidelines:
        - Chapter Description: {chapter_info['description']}
        - Target Length: Approximately {book_data.get('chapter_length', 2000)} words
        - Tone: {book_data.get('tone', 'Engaging and appropriate for the genre')}
        
        Book Outline Context:
        {outline[:1000]}...  # Provide context from outline
        
        Write a complete, engaging chapter that fits well within the overall book structure. 
        Include proper pacing, character development (if applicable), and advance the main theme or plot.
        """
        
        return self.generate_content(provider, prompt, max_tokens=3000)

# Initialize the book generator
book_gen = BookGenerator()

# Auto-configure APIs from environment variables if available
auto_config = {}
if OPENAI_API_KEY:
    auto_config['openai_key'] = OPENAI_API_KEY
if GEMINI_API_KEY:
    auto_config['gemini_key'] = GEMINI_API_KEY
if ANTHROPIC_API_KEY:
    auto_config['anthropic_key'] = ANTHROPIC_API_KEY

if auto_config:
    book_gen.configure_apis(auto_config)
    logger.info(f"Auto-configured APIs from environment: {list(auto_config.keys())}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure-apis', methods=['POST'])
def configure_apis():
    """Configure API keys"""
    try:
        api_configs = request.json
        success = book_gen.configure_apis(api_configs)
        
        if success:
            # Store in session for this demo (use proper database in production)
            session['api_configured'] = True
            return jsonify({'success': True, 'message': 'APIs configured successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to configure APIs'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/create-outline', methods=['POST'])
def create_outline():
    """Create book outline"""
    try:
        data = request.json
        provider = data['provider']
        book_data = data['book_data']
        
        outline = book_gen.create_book_outline(provider, book_data)
        
        return jsonify({
            'success': True,
            'outline': outline,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Outline creation error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error creating outline: {str(e)}'})

@app.route('/generate-chapter', methods=['POST'])
def generate_chapter():
    """Generate a single chapter"""
    try:
        data = request.json
        provider = data['provider']
        book_data = data['book_data']
        chapter_info = data['chapter_info']
        outline = data.get('outline', '')
        
        chapter_content = book_gen.generate_chapter(provider, book_data, chapter_info, outline)
        
        return jsonify({
            'success': True,
            'content': chapter_content,
            'chapter_number': chapter_info['number'],
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Chapter generation error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating chapter: {str(e)}'})

@app.route('/generate-full-book', methods=['POST'])
def generate_full_book():
    """Generate complete book (this is a simplified version - in production, use background tasks)"""
    try:
        data = request.json
        provider = data['provider']
        book_data = data['book_data']
        
        # Create outline first
        outline = book_gen.create_book_outline(provider, book_data)
        
        # For demo purposes, generate first 3 chapters
        # In production, you'd want to use background tasks for this
        chapters = []
        num_chapters = min(3, book_data.get('num_chapters', 3))  # Limit for demo
        
        for i in range(1, num_chapters + 1):
            chapter_info = {
                'number': i,
                'title': f'Chapter {i}',
                'description': f'Chapter {i} content based on the outline'
            }
            
            chapter_content = book_gen.generate_chapter(provider, book_data, chapter_info, outline)
            chapters.append({
                'number': i,
                'title': chapter_info['title'],
                'content': chapter_content
            })
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        return jsonify({
            'success': True,
            'outline': outline,
            'chapters': chapters,
            'total_chapters': len(chapters),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Full book generation error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating book: {str(e)}'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
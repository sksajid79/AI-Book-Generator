# AI Book Generator Web Application

A powerful web application that leverages multiple AI providers (OpenAI, Google Gemini, and Anthropic) to generate complete books based on your specifications.

## Features

- 🤖 **Multiple AI Provider Support**: Choose between OpenAI GPT-4, Google Gemini, or Anthropic Claude
- 📚 **Complete Book Generation**: Create full books with outlines, chapters, and structured content
- 🎨 **Customizable Parameters**: Control genre, length, tone, target audience, and more
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- ⚡ **Real-time Generation**: Watch your book come to life in real-time
- 💾 **Download Options**: Export your generated content as text files

## Prerequisites

- Python 3.8 or higher
- API keys for at least one of the following services:
  - OpenAI API (for GPT-4)
  - Google Gemini API
  - Anthropic API (for Claude)

## Installation

1. **Clone or download the project files**:
   ```bash
   mkdir ai-book-generator
   cd ai-book-generator
   ```

2. **Create the project structure**:
   ```
   ai-book-generator/
   ├── app.py
   ├── requirements.txt
   └── templates/
       └── index.html
   ```

3. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv book_generator_env
   
   # On Windows:
   book_generator_env\Scripts\activate
   
   # On macOS/Linux:
   source book_generator_env/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## API Keys Setup

You'll need to obtain API keys from the providers you want to use:

### OpenAI (GPT-4)
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create an account and get your API key
3. Format: `sk-...`

### Google Gemini
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a project and get your API key
3. Format: `AI...`

### Anthropic (Claude)
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account and get your API key
3. Format: `sk-ant-...`

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

3. **Follow the guided process**:
   - Step 1: Configure your API keys
   - Step 2: Enter book details (title, genre, theme, etc.)
   - Step 3: Select AI provider and generation type
   - Step 4: Watch your book generate and download results

## Usage Guide

### Step 1: API Configuration
- Enter API keys for the providers you want to use
- You only need at least one API key to proceed
- Keys are stored temporarily and securely

### Step 2: Book Details
Fill out the book information:
- **Title**: Your book's title
- **Genre**: Fiction, Non-fiction, Mystery, etc.
- **Target Audience**: Age group and demographic
- **Length**: Word count estimate
- **Theme/Plot**: Main story or concept
- **Chapters**: Number of chapters (3-50)
- **Tone**: Writing style preference

### Step 3: AI Provider Selection
- Choose your preferred AI provider
- Select generation type:
  - **Outline Only**: Creates a detailed book outline (recommended first step)
  - **Complete Book**: Generates full chapters (may take longer)
  - **Chapter by Chapter**: Generate individual chapters

### Step 4: Generation and Download
- Monitor the generation process
- Download your content as text files
- Continue generating more chapters if needed

## Generation Options

### Outline Generation
Perfect for planning your book:
- Detailed chapter breakdown
- Character descriptions
- Plot points and structure
- Style recommendations

### Full Book Generation
Complete book creation:
- Book outline
- Multiple chapters
- Coherent narrative flow
- Professional formatting

### Chapter by Chapter
Granular control:
- Generate specific chapters
- Refine individual sections
- Build your book incrementally

## File Structure

```
project/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend web interface
└── README.md          # This file
```

## API Endpoints

- `GET /` - Main web interface
- `POST /configure-apis` - Configure API keys
- `POST /create-outline` - Generate book outline
- `POST /generate-chapter` - Generate single chapter
- `POST /generate-full-book` - Generate complete book
- `GET /health` - Health check endpoint

## Customization Options

### Book Parameters
- **Genre**: 12+ different genres supported
- **Target Audience**: From children to professionals
- **Length**: 10K to 100K+ words
- **Chapters**: Flexible chapter count
- **Tone**: Professional to humorous styles

### AI Provider Features
- **OpenAI GPT-4**: Most creative and versatile
- **Google Gemini**: Fast and efficient generation
- **Anthropic Claude**: Thoughtful and detailed writing

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Verify your API keys are correct
   - Check your account has sufficient credits
   - Ensure API access is enabled

2. **Generation Timeouts**:
   - Try smaller chapters or shorter books
   - Use outline generation first
   - Check your internet connection

3. **Memory Issues**:
   - Reduce chapter length
   - Generate fewer chapters at once
   - Restart the application

### Error Messages

- **"APIs not configured"**: Enter valid API keys in Step 1
- **"Generation failed"**: Check API key validity and account status
- **"Timeout error"**: Try smaller generation requests

## Security Notes

- API keys are stored temporarily during your session
- Keys are not logged or permanently stored
- Use environment variables for production deployment
- Consider rate limiting for production use

## Performance Tips

1. **Start with outlines** before generating full content
2. **Use shorter chapters** for faster generation
3. **Test with one provider** before trying multiple
4. **Generate incrementally** rather than all at once

## Production Deployment

For production use, consider:

1. **Environment Variables**:
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY')
   ```

2. **Database Storage**: Replace session storage with database
3. **Background Tasks**: Use Celery for long-running generation
4. **Rate Limiting**: Implement API rate limiting
5. **Error Logging**: Add comprehensive error logging
6. **HTTPS**: Use SSL certificates for secure communication

## Contributing

Feel free to enhance this application:
- Add more AI providers
- Improve the UI/UX
- Add export formats (PDF, EPUB)
- Implement user accounts
- Add collaborative features

## License

This project is open source. Please ensure you comply with the terms of service for each AI provider you use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API keys and account status
3. Review the error messages in the browser console
4. Test with a simple book generation first

---

**Happy Book Writing! 📚✨**
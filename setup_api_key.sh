#!/bin/bash

echo "🔑 Setting up Hugging Face API Key for Image AI Detector"
echo "========================================================"
echo ""

# Check if API key is already set
if [ ! -z "$HF_API_KEY" ]; then
    echo "✅ HF_API_KEY is already set:"
    echo "   ${HF_API_KEY:0:10}..."
    echo ""
    echo "To use a different key, please unset it first:"
    echo "   unset HF_API_KEY"
    echo ""
    exit 0
fi

echo "📋 To get your Hugging Face API key:"
echo "1. Go to https://huggingface.co/settings/tokens"
echo "2. Click 'New token'"
echo "3. Give it a name (e.g., 'Image AI Detector')"
echo "4. Select 'Read' permissions"
echo "5. Copy the generated token (starts with 'hf_')"
echo ""

read -p "🔑 Paste your Hugging Face API key (starts with 'hf_'): " api_key

# Validate the API key format
if [[ $api_key =~ ^hf_[A-Za-z0-9]{20,}$ ]]; then
    echo ""
    echo "✅ Valid API key format detected!"
    echo ""
    
    # Set the environment variable
    export HF_API_KEY="$api_key"
    
    # Add to shell config for persistence
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "export HF_API_KEY=\"$api_key\"" >> ~/.zshrc
        echo "📝 Added to ~/.zshrc for persistence"
    else
        echo "export HF_API_KEY=\"$api_key\"" >> ~/.bashrc
        echo "📝 Added to ~/.bashrc for persistence"
    fi
    
    echo ""
    echo "🚀 API key is now set! You can:"
    echo "   - Restart your terminal to load the key automatically"
    echo "   - Or run: source ~/.zshrc (or ~/.bashrc)"
    echo ""
    echo "🧪 Test the API:"
    echo "   curl http://localhost:5001/health"
    echo ""
    
else
    echo ""
    echo "❌ Invalid API key format!"
    echo "   Expected format: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo "   Please check your key and try again."
    echo ""
    exit 1
fi

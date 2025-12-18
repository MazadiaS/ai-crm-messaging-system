"""Quick test script to verify OpenAI API integration"""

import os
from openai import OpenAI

def test_openai_connection():
    """Test OpenAI API connection"""

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("💡 Set it with: export OPENAI_API_KEY='your-key-here'")
        return False

    print("🧪 Testing OpenAI API Connection...")
    print("=" * 50)

    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        print("✅ Client initialized")

        # Test API call
        print("\n📤 Sending test request to GPT-4o...")
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=100,
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a professional copywriter."},
                {"role": "user", "content": "Write a short birthday greeting for John, a CEO."}
            ]
        )

        # Extract response
        message = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        print("✅ Response received!")
        print("\n📝 Generated Message:")
        print("-" * 50)
        print(message)
        print("-" * 50)

        print(f"\n📊 Tokens Used: {tokens_used}")
        print(f"   - Prompt: {response.usage.prompt_tokens}")
        print(f"   - Completion: {response.usage.completion_tokens}")

        # Calculate cost
        input_cost = (response.usage.prompt_tokens / 1_000_000) * 2.5
        output_cost = (response.usage.completion_tokens / 1_000_000) * 10.0
        total_cost = input_cost + output_cost

        print(f"\n💰 Estimated Cost: ${total_cost:.6f}")

        print("\n" + "=" * 50)
        print("✅ OpenAI API Integration Working!")
        print("=" * 50)

        return True

    except Exception as e:
        print("\n❌ Error:", str(e))
        print("\n💡 Tips:")
        print("   - Check your API key is valid")
        print("   - Ensure you have credits in your OpenAI account")
        print("   - Verify your internet connection")
        return False


if __name__ == "__main__":
    test_openai_connection()

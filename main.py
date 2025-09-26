#!/usr/bin/env python3
"""
Cribl Control Plane SDK Sandbox - Main Entry Point

This is a sandbox environment for experimenting with the Cribl Control Plane Python SDK.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

def test_cribl_sdk():
    """Test the Cribl Control Plane SDK installation and basic functionality."""
    console = Console()
    
    try:
        # Import the Cribl SDK
        from cribl_control_plane import CriblControlPlane, models, errors
        console.print("✅ Cribl Control Plane SDK imported successfully!", style="green")
        
        # Check for environment variables
        server_url = os.getenv("CRIBL_SERVER_URL", "https://api.example.com")
        bearer_token = os.getenv("CRIBL_BEARER_TOKEN", "")
        
        console.print(f"📡 Server URL: {server_url}")
        if bearer_token:
            console.print("🔑 Bearer token: [REDACTED]", style="green")
        else:
            console.print("⚠️  No bearer token found in CRIBL_BEARER_TOKEN env var", style="yellow")
        
        # Create SDK client (but don't make actual API calls without token)
        if bearer_token:
            console.print("\n🔧 Initializing Cribl Control Plane client...")
            
            with CriblControlPlane(
                server_url=server_url,
                security=models.Security(
                    bearer_auth=bearer_token,
                ),
            ) as ccp_client:
                console.print("✅ Client initialized successfully!", style="green")
                console.print("🎯 Ready to make API calls!")
                
                # Example: List available endpoints (you can uncomment and modify as needed)
                # console.print("\n📋 Example API operations available:")
                # console.print("• ccp_client.lake_datasets.create()")
                # console.print("• ccp_client.lake_datasets.list()")
                # console.print("• And many more...")
                
        else:
            console.print("\n💡 To test API calls, set environment variables:")
            console.print("   export CRIBL_SERVER_URL='https://your-cribl-instance.com'")
            console.print("   export CRIBL_BEARER_TOKEN='your-api-token'")
            
    except ImportError as e:
        console.print(f"❌ Failed to import Cribl SDK: {e}", style="red")
        console.print("💡 Make sure the SDK is installed: pip install -r requirements.txt")
    except Exception as e:
        console.print(f"❌ Error testing SDK: {e}", style="red")

def main():
    """Main entry point for the Cribl SDK sandbox."""
    console = Console()
    
    # Display welcome message
    welcome_text = Text("Cribl Control Plane SDK Sandbox", style="bold blue")
    console.print(Panel(welcome_text, title="🚀 Welcome", expand=False))
    
    # Environment info
    env_table = Table(title="Environment Information")
    env_table.add_column("Property", style="cyan")
    env_table.add_column("Value", style="green")
    
    env_table.add_row("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    env_table.add_row("Working Directory", str(Path.cwd()))
    env_table.add_row("Environment Variables", str(len(os.environ)))
    
    # Check if running in devcontainer
    if os.getenv('CODESPACES'):
        env_table.add_row("Environment", "☁️  GitHub Codespaces")
    elif os.getenv('REMOTE_CONTAINERS'):
        env_table.add_row("Environment", "🐳 VS Code Dev Container")
    else:
        env_table.add_row("Environment", "💻 Local Machine")
    
    console.print(env_table)
    
    # Test Cribl SDK
    console.print("\n" + "="*60)
    console.print("🧪 Testing Cribl Control Plane SDK")
    console.print("="*60)
    
    test_cribl_sdk()
    
    console.print("\n" + "="*60)
    console.print("📝 Next Steps:")
    console.print("1. Set your Cribl API credentials in environment variables")
    console.print("2. Modify this file to experiment with different SDK features")
    console.print("3. Check the examples/ directory in the SDK repo for more samples")
    console.print("4. Refer to: https://github.com/criblio/cribl_control_plane_sdk_python")
    console.print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)

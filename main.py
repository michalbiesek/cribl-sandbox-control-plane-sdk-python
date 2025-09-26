#!/usr/bin/env python3
"""
Cribl Control Plane SDK Sandbox - Main Entry Point

This example demonstrates OAuth2 authentication with Cribl.Cloud using the official SDK.
"""

import asyncio
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Import Cribl SDK components
try:
    from cribl_control_plane import CriblControlPlane
    from cribl_control_plane.models import Security, SchemeClientOauth
    SDK_AVAILABLE = True
except ImportError as e:
    SDK_AVAILABLE = False
    SDK_IMPORT_ERROR = str(e)

def show_environment_info():
    """Display environment information."""
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

async def cribl_cloud_example():
    """
    Example using OAuth2 authentication with Cribl.Cloud.
    
    This demonstrates how to:
    1. Set up OAuth2 authentication
    2. Create an authenticated SDK client
    3. Make API calls (list git branches)
    4. Handle common errors
    """
    console = Console()
    
    if not SDK_AVAILABLE:
        console.print(f"❌ Failed to import Cribl SDK: {SDK_IMPORT_ERROR}", style="red")
        console.print("💡 Make sure the SDK is installed: pip install -r requirements.txt")
        return

    console.print("✅ Cribl Control Plane SDK imported successfully!", style="green")
    
    # Cribl.Cloud configuration: Get from environment variables
    ORG_ID = os.getenv("CRIBL_ORG_ID", "your-org-id")
    CLIENT_ID = os.getenv("CRIBL_CLIENT_ID", "your-client-id")
    CLIENT_SECRET = os.getenv("CRIBL_CLIENT_SECRET", "your-client-secret")
    WORKSPACE_NAME = os.getenv("CRIBL_WORKSPACE_NAME", "main")

    base_url = f"https://{WORKSPACE_NAME}-{ORG_ID}.cribl.cloud/api/v1"
    console.print(f"📡 Server URL: {base_url}")

    # Check if we have real credentials
    if any(val.startswith("your-") for val in [ORG_ID, CLIENT_ID, CLIENT_SECRET]):
        console.print("⚠️  Using placeholder credentials. Set environment variables to test real API calls:", style="yellow")
        console.print("   • CRIBL_ORG_ID")
        console.print("   • CRIBL_CLIENT_ID") 
        console.print("   • CRIBL_CLIENT_SECRET")
        console.print("   • CRIBL_WORKSPACE_NAME (optional, defaults to 'main')")
        console.print("\n💡 Copy env.example to .env and fill in your values!")
        return

    try:
        console.print("🔧 Setting up OAuth2 authentication...")
        
        # Create authenticated SDK client with OAuth2
        client_oauth = SchemeClientOauth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            token_url="https://login.cribl.cloud/oauth/token",
            audience="https://api.cribl.cloud",
        )

        security = Security(client_oauth=client_oauth)
        client = CriblControlPlane(server_url=base_url, security=security)
        console.print("✅ Cribl SDK client created for Cribl.Cloud deployment", style="green")

        # Validate connection and list all git branches
        console.print("🔍 Testing connection by listing git branches...")
        response = await client.versions.branches.list_async()
        
        if response.items:
            branches = "\n\t".join([branch.id for branch in response.items])
            console.print(f"✅ Client works! Your list of branches:\n\t{branches}", style="green")
        else:
            console.print("✅ Client works! No branches found (this is normal for new deployments)", style="green")

    except Exception as error:
        status_code = getattr(error, "status_code", None)
        if status_code == 401:
            console.print("⚠️ Authentication failed! Check your CLIENT_ID and CLIENT_SECRET.", style="red")
        elif status_code == 429:
            console.print("⚠️ Uh oh, you've reached the rate limit! Try again in a few seconds.", style="yellow")
        else:
            console.print(f"❌ Something went wrong: {error}", style="red")

async def main():
    """Main entry point for the Cribl SDK sandbox."""
    console = Console()
    
    # Show environment info
    show_environment_info()
    
    # Test Cribl SDK with OAuth2
    console.print("\n" + "="*70)
    console.print("🧪 Testing Cribl Control Plane SDK with OAuth2 Authentication")
    console.print("="*70)
    
    await cribl_cloud_example()
    
    console.print("\n" + "="*70)
    console.print("📝 Next Steps:")
    console.print("1. Set your Cribl.Cloud OAuth2 credentials in environment variables")
    console.print("2. Modify this file to experiment with different SDK features")
    console.print("3. Check the SDK documentation for more API operations")
    console.print("4. Explore: https://github.com/criblio/cribl_control_plane_sdk_python")
    console.print("="*70)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)

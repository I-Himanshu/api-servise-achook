import requests
from typing import Dict, Optional
from datetime import datetime

class AlertSystemClient:
    def __init__(self, base_url: str = "http://localhost:3000"):
        """Initialize the Alert System client.
        
        Args:
            base_url (str): Base URL of the API. Defaults to localhost:3000
        """
        self.base_url = base_url.rstrip('/')

    def raise_alert(
        self,
        title: str,
        description: str,
        priority: str = "medium",
        assigned_to: Optional[str] = None
    ) -> Dict:
        """
        Raise a new alert using the API.
        
        Args:
            title (str): Title of the alert
            description (str): Detailed description of the alert
            priority (str, optional): Priority level (low/medium/high). Defaults to "medium"
            assigned_to (str, optional): Person assigned to the alert. Defaults to None
            
        Returns:
            Dict: Response from the API containing the created alert
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If required fields are missing or invalid
        """
        # Validate inputs
        if not title or not description:
            raise ValueError("Title and description are required")
            
        if priority.lower() not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of: low, medium, high")
            
        # Prepare request payload
        payload = {
            "title": title,
            "description": description,
            "priority": priority.lower(),
            "assignedTo": assigned_to
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/raiseIssue",
                json=payload
            )
            response.raise_for_status()  # Raise exception for error status codes
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error raising alert: {str(e)}")
            raise

    def get_alerts(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> Dict:
        """
        Get alerts with optional filters.
        
        Args:
            status (str, optional): Filter by status
            priority (str, optional): Filter by priority
            assigned_to (str, optional): Filter by assignee
            
        Returns:
            Dict: List of alerts matching the filters
        """
        params = {}
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority
        if assigned_to:
            params['assignedTo'] = assigned_to
            
        try:
            response = requests.get(
                f"{self.base_url}/getIssues",
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting alerts: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Create client instance
    client = AlertSystemClient()
    
    try:
        # Raise a new alert
        new_alert = client.raise_alert(
            title="Database Connection Error",
            description="Database connection timeout in production environment",
            priority="high", # Optional, defaults to "medium"
        )
        print("Created alert:", new_alert)
        
        # Get all high priority alerts
        high_priority_alerts = client.get_alerts(priority="high")
        print("\nHigh priority alerts:", high_priority_alerts)
        
        # Get all alerts assigned to Sarah
        sarah_alerts = client.get_alerts(assigned_to="Sarah")
        print("\nSarah's alerts:", sarah_alerts)
        
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {str(e)}")
from config import Config

class ApprovalEngine:
    # Configurable thresholds
    THRESHOLDS = {
        'MANAGER': float(getattr(Config, 'APPROVAL_THRESHOLD_MANAGER', 25000.0)),
        'FINANCE': float(getattr(Config, 'APPROVAL_THRESHOLD_FINANCE', 100000.0))
    }
    
    @staticmethod
    def get_required_approvals(amount):
        """Returns the required approval level based on amount."""
        if amount < ApprovalEngine.THRESHOLDS['MANAGER']:
            return "AUTO_APPROVED"
        elif amount < ApprovalEngine.THRESHOLDS['FINANCE']:
            return "MANAGER_APPROVAL"
        else:
            return "MANAGER_FINANCE_APPROVAL"

    @staticmethod
    def can_user_approve(user_role, required_approval):
        """
        Validates if a given role can approve the required level securely on the backend.
        Never trust frontend role information directly; this should check backend session role.
        """
        if required_approval == "AUTO_APPROVED":
            return True
        
        if user_role == "ADMIN":
            return True
            
        if required_approval == "MANAGER_APPROVAL":
            return user_role in ["MANAGER", "FINANCE"]
            
        if required_approval == "MANAGER_FINANCE_APPROVAL":
            return user_role == "FINANCE"
            
        return False

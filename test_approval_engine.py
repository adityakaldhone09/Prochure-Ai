import unittest
from services.approval_engine import ApprovalEngine

class TestApprovalEngine(unittest.TestCase):
    def test_thresholds(self):
        # Auto Approval (< 25,000)
        self.assertEqual(ApprovalEngine.get_required_approvals(20000), "AUTO_APPROVED") 
        self.assertEqual(ApprovalEngine.get_required_approvals(24999), "AUTO_APPROVED")
        
        # Manager Approval (25,000 to 100,000)
        self.assertEqual(ApprovalEngine.get_required_approvals(25000), "MANAGER_APPROVAL") 
        self.assertEqual(ApprovalEngine.get_required_approvals(50000), "MANAGER_APPROVAL") 
        self.assertEqual(ApprovalEngine.get_required_approvals(99999), "MANAGER_APPROVAL")
        
        # Manager + Finance Approval (>= 100,000)
        self.assertEqual(ApprovalEngine.get_required_approvals(100000), "MANAGER_FINANCE_APPROVAL") 
        self.assertEqual(ApprovalEngine.get_required_approvals(150000), "MANAGER_FINANCE_APPROVAL") 

    def test_permissions(self):
        # Auto Approved
        self.assertTrue(ApprovalEngine.can_user_approve("EMPLOYEE", "AUTO_APPROVED"))
        
        # Manager level
        self.assertFalse(ApprovalEngine.can_user_approve("EMPLOYEE", "MANAGER_APPROVAL"))
        self.assertTrue(ApprovalEngine.can_user_approve("MANAGER", "MANAGER_APPROVAL"))
        self.assertTrue(ApprovalEngine.can_user_approve("FINANCE", "MANAGER_APPROVAL"))
        
        # Finance level
        self.assertFalse(ApprovalEngine.can_user_approve("MANAGER", "MANAGER_FINANCE_APPROVAL"))
        self.assertTrue(ApprovalEngine.can_user_approve("FINANCE", "MANAGER_FINANCE_APPROVAL"))
        
        # Admin overrides
        self.assertTrue(ApprovalEngine.can_user_approve("ADMIN", "MANAGER_FINANCE_APPROVAL"))

if __name__ == '__main__':
    unittest.main()

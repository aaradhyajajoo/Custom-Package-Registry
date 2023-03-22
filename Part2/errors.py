class Err_Class(object):
    def set_error(self, code, msg):
        self.error_code = code
        self.error_msg = msg
        return {'message': msg}, code
    
    def malformed_req(self):
        return self.set_error(404, "Malformed request.")

    def unexpected_error(self):
        return {"code": -1, "message": "An error occurred while retrieving package"}, 500

    def package_exists(self):
        return self.set_error(409, "Package exists already.")
    
    def package_doesNot_exist(self):
        return self.set_error(404, "Package does not exist.")

    def auth_failure(self):
        return self.set_error(403, "Authentication failed.")
    
    def no_permission(self):
        return self.set_error(401, "You do not have permission to reset the registry.")
   


class Err_Class(object):
    def set_error(self, code, msg):
        self.error_code = code
        self.error_msg = msg
        return {'message': msg}, code

    def malformed_req(self):
        return self.set_error(404, "Malformed request.")

    def unexpected_error(self, metric):
        return self.set_error(500, f"The package rating system choked on at least one of the metrics. You can check {metric}")

    def package_exists(self):
        return self.set_error(409, "Package exists already.")

    def package_doesNot_exist(self):
        return self.set_error(404, "Package does not exist.")

    def auth_failure(self,bad_creds):
        if bad_creds:
            return self.set_error(403, 'Bad Credentials')
        return self.set_error(403, "Authentication failed.")

    def no_permission(self):
        return self.set_error(401, "You do not have permission to reset the registry.")

    def success(self):
        return self.set_error(201, "Success.")
    
    def missing_fields(self):
        return self.set_error(400, "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly (e.g. Content and URL are both set), or the AuthenticationToken is invalid.")

    def disqualified_rating(self,dis):
        return self.set_error(424,f"Package is not uploaded due to the disqualified rating for {dis}.")
    
    def too_many_packages(self):
        return self.set_error(413,"Too many packages returned.")
    
    def no_authentication(self):
        return self.set_error(501,"This system does not support authentication.")
    

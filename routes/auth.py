from flask import Blueprint

from controllers.authController import login, logout, register, requestPasswordReset, resetPassword, validatePasswordResetToken 

authRoutes = Blueprint('authRoutes', __name__)

authRoutes.route("/register", methods=["POST"]) (register)
authRoutes.route("/login", methods=['POST']) (login)
authRoutes.route("/logout", methods=['POST', "GET"]) (logout)

authRoutes.route("/requestPasswordReset", methods=["POST"]) (requestPasswordReset )
authRoutes.route("/validatePasswordResetToken", methods=["POST"]) (validatePasswordResetToken)
authRoutes.route("/resetPassword", methods=["POST"]) (resetPassword)
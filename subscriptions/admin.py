from django.contrib import admin

# # Register your models here.
# from .models import Plan, Customer, Coupon, Setting


# class PlanAdmin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     list_display = ("title", "max_connections", "monthly_campaigns", "max_messages","price","stripe_id")
# admin.site.register(Plan, PlanAdmin)


# class CustomerAdmin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     list_display = ("user","stripeid", "stripe_subscription_id", "cancel_at_period_end","membership","plan" )
# admin.site.register(Customer, CustomerAdmin)


# class CampaignAdmin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     list_display = ("user", "subject", "text", "status", "schedule", "pub_date")

# admin.site.register(Campaign, CampaignAdmin)

# class CouponAdmin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     list_display = ("name", "code","discount", "active","created")

# admin.site.register(Coupon, CouponAdmin)

# # class SettingAdmin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     # list_display = ("stripe_api_key")

# # admin.site.register(Setting, SettingAdmin)
# class SettingAdmin(admin.ModelAdmin):
#     list_display = ("stripe_api_key","publishable_key")
# admin.site.register(Setting, SettingAdmin)

# class LinkedinProfileAdmin(admin.ModelAdmin):
#     list_display = ("user","fullname", "linkedin_email")
# admin.site.register(LinkedinProfile, LinkedinProfileAdmin)

# class ConnectionAdmin(admin.ModelAdmin):
#     list_display = ("user","firstname", "lastname", "company", "position")
# admin.site.register(Connection, ConnectionAdmin)


# class MessageAdmin(admin.ModelAdmin):
#     list_display = ("sender","campaign","message","connection", "status", "pub_date")
    
#     # def sender(self, obj):
#     #     return obj.campaign.user
    
#     def message(self, obj):
#         return obj.campaign.text
    
#     def get_connection(self, obj):
#         return obj.connection.firstname + " " + obj.connection.lastname
        
# admin.site.register(Message, MessageAdmin)


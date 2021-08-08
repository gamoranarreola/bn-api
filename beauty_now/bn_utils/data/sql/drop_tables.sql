DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;

DROP TABLE IF EXISTS authtoken_token CASCADE;

DROP TABLE IF EXISTS beautiers_beautier CASCADE;
DROP TABLE IF EXISTS beautiers_beautierspecialty CASCADE;
DROP TABLE IF EXISTS beautiers_specialty CASCADE;

DROP TABLE IF EXISTS clients_client CASCADE;

DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;

DROP TABLE IF EXISTS oauth2_provider_accesstoken CASCADE;
DROP TABLE IF EXISTS oauth2_provider_application CASCADE;
DROP TABLE IF EXISTS oauth2_provider_grant CASCADE;
DROP TABLE IF EXISTS oauth2_provider_refreshtoken CASCADE;
DROP TABLE IF EXISTS oauth2_provider_idtoken CASCADE;

DROP TABLE IF EXISTS bn_app_service CASCADE;
DROP TABLE IF EXISTS bn_app_servicecategory CASCADE;
DROP TABLE IF EXISTS bn_app_service_specialties CASCADE;
DROP TABLE IF EXISTS bn_app_specialty CASCADE;

DROP TABLE IF EXISTS social_auth_association CASCADE;
DROP TABLE IF EXISTS social_auth_code CASCADE;
DROP TABLE IF EXISTS social_auth_nonce CASCADE;
DROP TABLE IF EXISTS social_auth_partial CASCADE;
DROP TABLE IF EXISTS social_auth_usersocialauth CASCADE;

DROP TABLE IF EXISTS bn_app_authuser CASCADE;
DROP TABLE IF EXISTS bn_app_authuser_groups CASCADE;
DROP TABLE IF EXISTS bn_app_authuser_user_permissions CASCADE;

DROP TABLE IF EXISTS bn_app_lineitem CASCADE;
DROP TABLE IF EXISTS bn_app_workorder CASCADE;
DROP TABLE IF EXISTS bn_app_workorder_line_items CASCADE;

DROP TABLE IF EXISTS bn_app_beautierprofile CASCADE;
DROP TABLE IF EXISTS bn_app_beautierprofile_specialties CASCADE;
DROP TABLE IF EXISTS bn_app_customeraddress CASCADE;
DROP TABLE IF EXISTS bn_app_customerprofile CASCADE;
DROP TABLE IF EXISTS bn_app_customerprofileaddress CASCADE;

DROP TABLE IF EXISTS bn_app_lineitem_staffing_assignments CASCADE;
DROP TABLE IF EXISTS bn_app_staffingassignment CASCADE;
DROP TABLE IF EXISTS bn_app_staffingassignment_beautier_profiles CASCADE;

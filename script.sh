aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH \
--client-id 567fvtgipn0tk6tpldhr4jo0t1 \
--auth-parameters USERNAME=user@test.com,PASSWORD=1234567aB@


Jordan.Eisenman@nrel.gov
1234567aB@

aws cognito-idp initiate-auth \
    --client-id 567fvtgipn0tk6tpldhr4jo0t1 \
    --auth-flow USER_PASSWORD_AUTH \
    --auth-parameters "{\"USERNAME\":\"Jordan.Eisenman@nrel.gov\",\"PASSWORD\":\"1234567aB@\"}" \
    --region us-west-2

aws cognito-idp admin-set-user-password \
    --user-pool-id us-west-2_TvEJ1biz0 \
    --username Jordan.Eisenman@nrel.gov \
    --password 1234567aB@1 \
    --permanent 1234567aB@1 \
    --region us-west-2


aws cognito-idp admin-set-user-password \
  --user-pool-id us-west-2_TvEJ1biz0 \
  --username Jordan.Eisenman@nrel.gov \
  --password "1234567aB@" \
  --permanent "1234567aB@2" \
  --region us-west-2



  admin-reset-user-password
--user-pool-id <value>
--username <value>

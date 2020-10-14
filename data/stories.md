## start
* greet
 - begin_form
 - form{"name":"begin_form"}
 - form{"name":null}
> part_one

## step 2 to 4
> part_one
* affirm
  - step2_form
  - form{"name":"step2_form"}
  - form{"name":null}
## step 5
  - health_form
  - form{"name":"begin_form"}
  - form{"name":null}
>part_four

## step 6
>part_four
  - action_set_reminder
  - additional_form
  - form{"name":"additional_form"}
  - form{"name":null}

## debug
* deny
  - sub_health_form
  - form{"name":"sub_health_form"}
  - form{"name":null}
## bot challenge
* bot_challenge
  - utter_iamabot

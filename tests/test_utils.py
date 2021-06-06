import json
import configparser
from jsonvalidator.utils import load_schema, validate_schema, merge_events


config = configparser.ConfigParser()
config_file = '/jsonvalidator/config/demo.cfg'
config.read(config_file)
schema_file = config['project_info']['schema_file']

# Load schema from file
schema = load_schema(schema_file)


def test_valid_schema():
    """
    Test valid input json
    """
    input_json = json.loads("""
         {"id": "FB16866D-AE4D-416F-8848-122B07DA42F5", "received_at": "2018-01-30 18:13:52.221000", "anonymous_id": "0A52CDC6-DDDC-4F7D-AA24-4447F6AF2689",  
         "context_app_version": "1.2.3",  "context_device_ad_tracking_enabled": true,  "context_device_manufacturer": "Apple",   "context_device_model": "iPhone8,4",  
         "context_device_type": "android",  "context_library_name": "analytics-ios","context_library_version":"3.6.7", "context_locale": "de-DE",  
         "context_network_wifi": true,  "context_os_name": "android",   "context_timezone": "Europe/Berlin", "event": "submission_success",  
         "event_text": "submissionSuccess", "original_timestamp": "2018-01-30T19:13:43.383+0100",   "sent_at": "2018-01-30 18:13:51.000000",  
         "timestamp": "2018-01-30 18:13:43.627000",  "user_id": "18946",  "context_network_carrier": "o2-de",  "context_device_token": null,  
         "context_traits_taxfix_language": "en-DE"}
        """)
    is_valid, message = validate_schema(input_json, schema)
    assert is_valid == True


def test_invalid_boolean_field():
    """
    Test invalid json with wrong data type for boolean field
    context_device_ad_tracking_enabled should be boolean
    """
    input_json = json.loads("""
             {"id": "AED96FC7-19F1-46AB-B79F-D412117119BD",  "received_at": "2018-01-30 18:28:12.378000",  "anonymous_id": "8E0302A3-2184-4592-851D-B93C32E410AB", 
             "context_app_version": "1.2.3", "context_device_ad_tracking_enabled": "404", "context_device_manufacturer": "Apple", "context_device_model": "iPhone8,4", 
             "context_device_type": "ios",  "context_library_name": "analytics-ios","context_library_version":"3.6.7", "context_timezone": "Europe/Berlin", 
             "context_locale": "de-DE",  "context_network_wifi": true,  "context_os_name": "iOS",  "event":"registration_initiated", "event_text": "registrationInitiated", 
             "original_timestamp": "2018-01-30T19:28:06.291+0100",  "sent_at":"2018-01-30 18:28:12.000000", "timestamp": "2018-01-30 18:28:06.561000", "user_id": "18234", 
             "context_network_carrier": "o2-de",  "context_device_token": null, "context_traits_taxfix_language": "de-DE"}
            """)
    is_valid, error_message = validate_schema(input_json, schema)
    assert is_valid == False
    assert error_message == "'404' is not of type 'boolean'"


def test_invalid_string_field():
    """
    Test invalid json with wrong data type for string field
    context_os_name should be a string
    """
    input_json = json.loads("""
             {"id": "FB16866D-AE4D-416F-8848-122B07DA42F5", "received_at": "2018-01-30 18:13:52.221000", "anonymous_id": "0A52CDC6-DDDC-4F7D-AA24-4447F6AF2689",  
             "context_app_version": "1.2.3",  "context_device_ad_tracking_enabled": true,  "context_device_manufacturer": "Apple",   "context_device_model": "iPhone8,4",  
             "context_device_type": "android",  "context_library_name": "analytics-ios","context_library_version":"3.6.7", "context_locale": "de-DE",  
             "context_network_wifi": true,  "context_os_name": 5.6,   "context_timezone": "Europe/Berlin", "event": "submission_success",  
             "event_text": "submissionSuccess", "original_timestamp": "2018-01-30T19:13:43.383+0100",   "sent_at": "2018-01-30 18:13:51.000000",  
             "timestamp": "2018-01-30 18:13:43.627000",  "user_id": "18946",  "context_network_carrier": "o2-de",  "context_device_token": null,  
             "context_traits_taxfix_language": "en-DE"}
            """)
    is_valid, error_message = validate_schema(input_json, schema)
    assert is_valid == False
    assert error_message == "5.6 is not of type 'string'"


def test_missing_field():
    """
    Test invalid json with missing field
    'id' should be present in input doc
    """
    input_json = json.loads("""
                 {"received_at": "2018-01-30 18:28:12.378000",  "anonymous_id": "8E0302A3-2184-4592-851D-B93C32E410AB", 
                 "context_app_version": "1.2.3", "context_device_ad_tracking_enabled": "404", "context_device_manufacturer": "Apple", "context_device_model": "iPhone8,4", 
                 "context_device_type": "ios",  "context_library_name": "analytics-ios","context_library_version":"3.6.7", "context_timezone": "Europe/Berlin", 
                 "context_locale": "de-DE",  "context_network_wifi": true,  "context_os_name": "iOS",  "event":"registration_initiated", "event_text": "registrationInitiated", 
                 "original_timestamp": "2018-01-30T19:28:06.291+0100",  "sent_at":"2018-01-30 18:28:12.000000", "timestamp": "2018-01-30 18:28:06.561000", "user_id": "18234", "context_network_carrier": "o2-de",  "context_device_token": null, "context_traits_taxfix_language": "de-DE"}
                """)
    is_valid, error_message = validate_schema(input_json, schema)
    assert is_valid == False
    assert error_message == "'id' is a required property"


def test_merge_documents():
    """
    Test merging documents
    Read json records from file and check the merged output
    """
    events_merged = {}
    with open('/jsonvalidator/tests/resources/test_input.json') as infile:
        for row in infile:
            row = json.loads(row)
            events_merged = merge_events(events_merged, row)
    expected_output = {'2018-01-30': {'submission_success': 3, 'registration_initiated': 2}, '2018-01-31': {'submission_success': 1}}
    assert events_merged == expected_output
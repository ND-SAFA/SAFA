/************************************************************************************************ 
This may be outdated (Using a reference from nightwatch 1.0.0), but I will update once a few more additons are tested 
  Some Notes:
    - This Version of Nightwatch only suports Chrome at the moment, with it using chromeDriver 99+
    - preveious testing folder has been changed to allow nightwatch to run tests
***********************************************************************************************/
module.exports = {
  'src_folders': ['tests/e2e/nightwatch'],
  'page_objects_path': ['tests/e2e/nightwatch/page-objects'],

  'webdriver': {
      'start_process': true,
      'server_path': require('chromedriver').path,
      'port': 9515
  },

  'test_settings': {
      'default': {
          'screenshots': {
              'enabled': true,
              'on_failure': true,
              'on_error': true,
              'path': 'tests_output/screenshots'
          }, 
          'desiredCapabilities': {
              'browserName': 'chrome',
              /*'chromeOptions': {
                  'args': ['--headless']
              } */
          }
      }
  }
};
Feature: Iperf Configspec
 Scenario Outline: client/server options
   Given a configspec with a <state> <option> option
   When the configspec is validated
   Then the configspec outcome is <outcome>

 Examples: client/server 
 | state   | option        | outcome        |
 | valid   | format        | as expected    |
 | invalid | format        | False          |
 | missing | format        | None           |
 | valid   | interval      | positive float |
 | invalid | interval      | False          |
 | missing | interval      | None           |
 | valid   | len           | as expected    |
 | invalid | len           | False          |
 | missing | len           | None           |
 | valid   | print_mss     | True           |
 | invalid | print_mss     | False          |
 | missing | print_mss     | None           |
 | valid   | output        | as expected    |
 | missing | output        | None           |
 | valid   | port          | as expected    |
 | invalid | port          | False          |
 | valid   | udp           | True           |
 | valid   | window        | as expected    |
 | invalid | window        | False          |
 | valid   | bind          | as expected    |
 | missing | bind          | None           |
 | valid   | compatibility | True           |
 | valid   | mss           | as expected    |
 | invalid | mss           | False          |
 | valid   | nodelay       | True           |
 | valid   | IPv6Version   | True           |

 Examples: server only
 | state | option     | outcome |
 | valid | single_udp | True    |
 | valid | daemon     | True    |

 Examples: client only
 | state   | option           | outcome        |
 | valid   | bandwidth        | as expected    |
 | invalid | bandwidth        | False          |
 | valid   | dualtest         | True           |
 | valid   | num              | as expected    |
 | invalid | num              | False          |
 | valid   | tradeoff         | True           |
 | valid   | time             | positive float |
 | invalid | time             | False          |
 | valid   | fileinput        | as expected    |
 | missing | fileinput        | None           |
 | invalid | fileinput        | False          |
 | valid   | listenport       | as expected    |
 | invalid | listenport       | False          |
 | valid   | parallel         | as expected    |
 | invalid | parallel         | False          |
 | valid   | ttl              | as expected    |
 | valid   | linux-congestion | as expected    |

 Examples: miscellaneous
 | state   | option        | outcome     |
 | valid   | reportexclude | as expected |
 | invalid | reportexclude | False       |
 | valid   | reportstyle   | as expected |
 | invalid | reportstyle   | False       |

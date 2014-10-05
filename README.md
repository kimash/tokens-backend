## Tokens Game - Back-End Web UI

[Live Site](http://tokensgame-web-ui.herokuapp.com/)


### Description

This web UI allows users to create a series of game rounds for a public policy tokens game. Each round has a series of yes/no questions. Each answer returns a different outcome with respect to the tokens affected. Some answers will add tokens, others will subtract them. For example:

* Should we build more schools?

	- income tax: Yes: +5, No: -3 
    - education level: Yes: +3, No: -4 
    - public health: Yes: +2, No: -5 
    - entrepreneurship: Yes: +3, No: -1 
    - community art: Yes: -3, No: +4 
    - immigration: Yes: 0, No: 0
    
Front-end implementation can be found here:

### License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>




### Step 2 : Adding MongoLabs to your Heroku App

Heroku offers a [lot of different Add-ons](https://addons.heroku.com/) for your apps. Many different types of databases, image tools, cache utilities are available from 3rd party companies. Many offer a trial plan to test and develop with before you commit to a paid plan.

MongoLabs offers a [500MB MongoDB instance for free](https://addons.heroku.com/mongolab) (see here) : ) How wonderful.

To install the MongoLabs 

* Navigate to the code folder of your app
* In Terminal, add the MongoLab starter plan

		heroku addons:add mongolab:sandbox


# Cloudfront

## Enablement Options

Use a separate CNAME for static content
- Static content cached, dynamic content straght from origin
- Most efficient
- More effort to set up and manage

Point entire URL to CloudFront
- Easiest to manage
- Use URL patterns to stage dynamic content 
- ALL content goes through edge locations

## How to expire contents

Time to live(TTL)
- Fixed period of time (expiration period)
- Time period is set by you
- GET request to origin from CloudFront wlil use ``if-Modified-Since header``

Change object name
- Header-v1.jpg becomes Header-v2.jpg
- New name forces refresh

Invalidate object
- Last resort: very inefficient and very expensive
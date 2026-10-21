SAHYADRI MIST RETREAT - homestay / resort website (SAMPLE CONTENT)

FOLDERS
  site/        the finished website - upload this
  build.py     the generator - all text/prices/rooms are in the CONTENT block at the top
  assets/      source CSS + JS

TO MAKE IT A REAL CLIENT'S SITE
  1. Open build.py, edit the CONTENT block (name, phone, WhatsApp number, address, rooms, prices,
     reviews, FAQs, policies, domain, Google Analytics ID).
  2. Put real photos in site/assets/img/ using the same file names (or set IMG_EXT = "webp"/"jpg"
     in build.py and drop photos in). Convert photos to WebP, ~1600px wide, under 250 KB each.
  3. Run:  python3 build.py
  4. Upload the site/ folder to Netlify (drag & drop), Vercel, Cloudflare Pages or any host.
     To preview locally:  cd site && python3 -m http.server   then open http://localhost:8000

IMPORTANT
  - The reviews are SAMPLES. Use only genuine guest reviews before going live.
  - Images are generated placeholder artwork until you add real photos.
  - Enquiry form opens WhatsApp with the details pre-filled (no backend needed).
  - Tracked events (GA4 / dataLayer): whatsapp_click, phone_click, email_click, enquiry_submit, cta_click.

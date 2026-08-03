def generate_ai_image(self, headline: str, category: str) -> Image.Image | None:
        try:
            clean_headline = headline.encode("ascii", "ignore").decode("ascii")
            if not clean_headline.strip():
                clean_headline = "breaking news update"
                
            # Menggunakan prompt gaya ilustrasi karikatur komik satir klasik sesuai referensi
            prompt = f"Classic satirical comic caricature illustration about {clean_headline}, bold black outlines, retro vintage earthy color palette, expressive storytelling art style, high quality"
            encoded_prompt = quote(prompt)
            ai_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={WIDTH}&height={HEIGHT}&nologo=true&seed=42"
            
            logger.info("Membuat gambar karikatur satir via Pollinations: %s", clean_headline[:30])
            r = requests.get(ai_url, timeout=30)
            if r.status_code == 200:
                return Image.open(BytesIO(r.content)).convert("RGB")
            else:
                logger.warning("Pollinations AI merespon dengan status code: %s", r.status_code)
        except Exception as e:
            logger.warning("Gagal membuat gambar karikatur dari Pollinations: %s", e)
        return None

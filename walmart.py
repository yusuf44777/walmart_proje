import streamlit as st
import google.generativeai as genai
import openai
import os

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Walmart Ürün Açıklaması Üreteci",
    page_icon="🛒",
    layout="wide"
)

# Başlık
st.title("🛒 Walmart Ürün Açıklaması Üreteci")
st.subheader("Google Gemini AI ile ürün başlığı, temel özellikler ve açıklama oluşturun")

# Sidebar - API Key girişi ve model seçimi
st.sidebar.header("🔧 Ayarlar")

# Model seçimi
selected_model = st.sidebar.selectbox(
    "AI Model Seçin:",
    ["Google Gemini", "OpenAI ChatGPT"],
    help="Kullanmak istediğiniz AI modelini seçin"
)

if selected_model == "Google Gemini":
    api_key = st.sidebar.text_input(
        "Google Gemini API Key:",
        type="password",
        help="Google AI Studio'dan API anahtarınızı alın"
    )
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0')

else:  # OpenAI ChatGPT
    api_key = st.sidebar.text_input(
        "OpenAI API Key:",
        type="password",
        help="OpenAI Platform'dan API anahtarınızı alın"
    )

# Ana içerik
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Ürün Bilgileri")
    
    # Ürün özelliklerini girme formu
    with st.form("product_form"):
        product_name = st.text_input("Ürün Adı:", placeholder="Örn: Sony WH-1000XM4 Wireless Bluetooth Headphones")
        
        product_features = st.text_area(
            "Ürün Özellikleri:",
            placeholder="Ürünün tüm özelliklerini, markasını ve faydalarını detaylı bir şekilde yazın...\nÖrn: Sony marka, aktif gürültü engelleme teknolojisi, 30 saat pil ömrü, hızlı şarj özelliği, dokunmatik kontroller, ses kalitesi, kablosuz bağlantı, konfor",
            height=150,
            help="Ürün adı, marka, özellikler ve müşterilerin arayabileceği anahtar kelimeleri ekleyin"
        )
        
        submit_button = st.form_submit_button("🚀 Açıklama Oluştur", use_container_width=True)

with col2:
    st.header("✨ Oluşturulan İçerik")
    
    if submit_button and api_key and product_name and product_features:
        with st.spinner("AI içerik oluşturuyor..."):
            try:
                # Prompt oluşturma
                prompt = f"""
                Walmart.com için aşağıdaki ürün bilgilerine göre profesyonel bir içerik oluştur:
                
                Ürün Adı: {product_name}
                Ürün Özellikleri: {product_features}
                
                Walmart standartlarına uygun olarak aşağıdaki formatı kullan:
                
                TITLE: [Walmart için SEO uyumlu, çekici bir başlık]
                
                KEY_FEATURES: [3-10 önemli özellik, her satırda bir özellik]
                
                DESCRIPTION: [Walmart standartlarına uygun ürün açıklaması - minimum 150 kelime]
                
                TITLE KURALLARI:
                - Maximum 100 karakter kısa başlık yaz
                - Net, açıklayıcı başlık oluştur
                - Tekrarlayan anahtar kelimeler, çoklu markalar kullanma
                - İlgili değerler ekle
                - Büyük harfle yazma veya özel karakterler kullanma (~, !, *, $ vb.)
                - Promotional claims kullanma (Free shipping, Hot sale, Top rated vb.)
                - Competitor exclusivity iddialarında bulunma
                - Irrelevant bilgi ekleme (Coming soon, Out-of-stock vb.)
                - URL ekleme (Walmart.com dahil)
                - External URL kullanma
                - Sadece İngilizce yaz
                - Yıl ekleme (2024, 2025 vb.) önerilen durumlar hariç
                
                KEY_FEATURES KURALLARI:
                - En önemli özellikleri önce listele (3-10 adet)
                - Kısa cümleler veya anahtar kelimeler kullan
                - Her özellik maximum 80 karakter olsun (boşluklar dahil)
                - Promotional claims kullanma (Free shipping, Hot sale, Top rated vb.)
                - Irrelevant bilgi ekleme (Coming soon, Out-of-stock vb.)
                - External URL kullanma
                - Emoji kullanma
                - HTML, bullet points veya numaralı liste formatı kullanma
                - Sadece İngilizce yaz
                - Ürün başlığında belirtilenden farklı bir ürün tanımlama
                
                DESCRIPTION KURALLARI:
                - Ürün adı, marka ve anahtar kelimeleri dahil et
                - Müşterilerin arayabileceği ilgili kelimeleri kullan
                - Minimum 150 kelimelik tek paragraf oluştur
                - Promotional claims kullanma (Free shipping, Hot sale, Premium quality vb.)
                - Competitor exclusivity iddialarında bulunma
                - Authenticity claims yapma
                - Emoji kullanma
                - Sadece İngilizce yaz
                - Ürün başlığında belirtilenden farklı bir ürün tanımlama
                - External URL veya irrelevant bilgi ekleme
                
                Tüm içerik İngilizce olsun ve Walmart'ın profesyonel tonunu yansıtsın.
                """
                
                # AI'dan yanıt al
                if selected_model == "Google Gemini":
                    response = model.generate_content(prompt)
                    content = response.text
                else:  # OpenAI ChatGPT
                    client = openai.OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a professional content writer for Walmart.com product listings."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=2000,
                        temperature=0.7
                    )
                    content = response.choices[0].message.content
                
                # İçeriği parse et
                sections = content.split('\n\n')
                title = ""
                key_features = ""
                description = ""
                
                for section in sections:
                    if section.startswith('TITLE:'):
                        title = section.replace('TITLE:', '').strip()
                    elif section.startswith('KEY_FEATURES:'):
                        key_features = section.replace('KEY_FEATURES:', '').strip()
                    elif section.startswith('DESCRIPTION:'):
                        description = section.replace('DESCRIPTION:', '').strip()
                
                # Sonuçları göster
                st.success("✅ İçerik başarıyla oluşturuldu!")
                
                # Title kutusu
                with st.container():
                    st.markdown("### 📍 Ürün Başlığı")
                    st.info(title if title else "Başlık oluşturulamadı")
                
                # Key Features kutusu
                with st.container():
                    st.markdown("### ⭐ Key Features")
                    st.warning(key_features if key_features else "Özellikler oluşturulamadı")
                
                # Description kutusu
                with st.container():
                    st.markdown("### 📄 Ürün Açıklaması")
                    st.success(description if description else "Açıklama oluşturulamadı")
                
                # İndirme seçenekleri
                st.markdown("---")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📋 Tümünü Kopyala"):
                        full_content = f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}"
                        st.code(full_content)
                
                with col_b:
                    if title:
                        st.download_button(
                            "💾 Metin Olarak İndir",
                            data=f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}",
                            file_name=f"{product_name}_walmart_content.txt",
                            mime="text/plain"
                        )
                
            except Exception as e:
                st.error(f"❌ Hata oluştu: {str(e)}")
                if selected_model == "Google Gemini":
                    st.info("Lütfen Google Gemini API anahtarınızı kontrol edin ve tekrar deneyin.")
                else:
                    st.info("Lütfen OpenAI API anahtarınızı kontrol edin ve tekrar deneyin.")
    
    elif submit_button:
        if not api_key:
            if selected_model == "Google Gemini":
                st.warning("⚠️ Lütfen Google Gemini API anahtarınızı girin.")
            else:
                st.warning("⚠️ Lütfen OpenAI API anahtarınızı girin.")
        elif not product_name:
            st.warning("⚠️ Lütfen ürün adını girin.")
        elif not product_features:
            st.warning("⚠️ Lütfen ürün özelliklerini girin.")

# Footer
st.markdown("---")
if selected_model == "Google Gemini":
    st.markdown(
        "🔧 **Geliştirici Notu:** Bu araç Google Gemini AI kullanarak Walmart için optimize edilmiş ürün içeriği oluşturur."
    )
else:
    st.markdown(
        "🔧 **Geliştirici Notu:** Bu araç OpenAI ChatGPT kullanarak Walmart için optimize edilmiş ürün içeriği oluşturur."
    )
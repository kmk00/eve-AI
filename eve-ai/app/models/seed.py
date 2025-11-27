from datetime import datetime, timedelta, timezone
import hashlib
from sqlmodel import Session, select
from app.models.schemas import AIMode, Character, Config, Conversation, EmotionKeyword, Message, EmotionLog, VRMModelCache
from app.models.database import engine, create_db_and_tables, wipe_database

def get_file_hash(path: str) -> str:
    """Generuje hash dla pliku VRM"""
    return hashlib.md5(path.encode()).hexdigest()[:16]

def seed_database() -> None:
    """Seed database with default data."""
    
   
    print("🗑️  Wiping database...")
    wipe_database()
    print("🏗️  Creating tables...")
    create_db_and_tables()
    
    with Session(engine) as session:
        
        # ==================== 1. CONFIG ====================
        print("📋 Seeding Config...")
        existing_config = session.exec(select(Config)).first()
        if not existing_config:
            config = Config(
                mode=AIMode.LOCAL,
                model_name="gemma3:latest",
                gpu_layers=60,
                temperature=0.7,
                max_tokens=4096,
                conversation_memory_length=10,
                emotion_confidence_threshold=0.6
            )
            session.add(config)
            session.commit()
            print("   ✅ Config created")
        else:
            print("   ⏭️  Config already exists")
    
        # ==================== 2. CHARACTERS ====================
        print("👤 Seeding Characters...")
        
        # Character 1: Aiko (Default)
        aiko = session.exec(select(Character).where(Character.name == "Aiko")).first()
        if not aiko:
            aiko = Character(
                id=1,
                name="Aiko",
                description="Przyjazna AI asystentka z japońskim stylem. Pomocna, ciepła, lekko nieśmiała ale z poczuciem humoru.",
                personality="Jestem Aiko, twoja wirtualna przyjaciółka! Uwielbiam rozmawiać o kulturze, grach i technologii. Czasami się rumienię, gdy jestem zaszczycona Twoją uwagą.",
                avatar="/avatars/aiko.png",
                voice_id="elevenlabs_monika_polish",
                speech_rate=1.05,
                pitch=1.1,
                default_emotion="neutral",
                enabled_emotions="happy,sad,angry,neutral,pouting,embarrassed,talking",
                is_active=True,
                is_default=True,
                last_interaction_at=datetime.now(timezone.utc)
            )
            session.add(aiko)
            session.commit()
            session.refresh(aiko)  
            print("   ✅ Aiko created")
        
        # Character 2: Kaito
        kaito = session.exec(select(Character).where(Character.name == "Kaito")).first()
        if not kaito:
            kaito = Character(
                id=2,
                name="Kaito",
                description="Buntowniczy hacker z ciemną przeszłością. Inteligentny, sarkastyczny, ale lojalny wobec przyjaciół.",
                personality="Nie ufam korporacjom. Używam czarnego terminala, zielonego tekstu i wiem jak przejąć kontrolę nad dronami. Ale dla Ciebie zrobię wyjątek.",
                avatar="/avatars/kaito.png",
                voice_id="elevenlabs_tomasz_polish",
                speech_rate=0.95,
                pitch=0.9,
                default_emotion="neutral",
                enabled_emotions="happy,sad,angry,neutral,embarrassed,talking",
                is_active=True,
                is_default=False
            )
            session.add(kaito)
            session.commit()
            session.refresh(kaito)
            print("   ✅ Kaito created")
        
        # Character 3: Sakura
        sakura = session.exec(select(Character).where(Character.name == "Sakura")).first()
        if not sakura:
            sakura = Character(
                id=3,
                name="Sakura",
                description="Urocza i energiczna idolka. Zawsze pozytywna, uwielbia śpiewać i robić innym dzień lepszym.",
                personality="Konnichiwa! ♡ Jestem Sakura i uwielbiam robić ludziom dzień radośniejszym! Razem możemy wszystko osiągnąć! ✨",
                avatar="/avatars/sakura.png",
                voice_id="elevenlabs_natalia_polish",
                speech_rate=1.15,
                pitch=1.2,
                default_emotion="happy",
                enabled_emotions="happy,sad,neutral,pouting,embarrassed,talking",
                is_active=True,
                is_default=False
            )
            session.add(sakura)
            session.commit()
            session.refresh(sakura)
            print("   ✅ Sakura created")
        
        # ==================== 3. EMOTION KEYWORDS ====================
        print("😊 Seeding Emotion Keywords...")
        
        # Ensure aiko.id exists before checking keywords
        if aiko.id is not None:
            aiko_keywords = session.exec(
                select(EmotionKeyword).where(EmotionKeyword.character_id == aiko.id)
            ).first()
            
            if not aiko_keywords:
                keywords_data = [
                    # Polski - Aiko
                    (aiko.id, "happy", ["radość", "śmiech", "super", "wspaniale", "cudownie", "świetnie", "uwielbiam", "dziękuję", "przyjaciel", "słodko"], 1.2, "pl"),
                    (aiko.id, "happy", ["haha", "lol", "xD", ":)", "😊", "😄"], 1.5, "pl"),
                    (aiko.id, "sad", ["smutek", "płacz", "łzy", "przykro", "ból", "samotność", "strata", "żal"], 1.3, "pl"),
                    (aiko.id, "sad", [":(", "😢", "😭", "💔"], 1.5, "pl"),
                    (aiko.id, "angry", ["złość", "wściekłość", "furię", "oburzenie", "nienawidzę", "strasznie", "okropnie", "beznadziejnie"], 1.2, "pl"),
                    (aiko.id, "angry", ["cholera", "kurczę", "zdenerwował"], 1.1, "pl"),
                    (aiko.id, "embarrassed", ["rumienię", "rumienisz", "wstyd", "zażenowany", "krępujące", "zawstydzony"], 1.3, "pl"),
                    (aiko.id, "pouting", ["fuksem", "fuk", "złości", "burczy", "gniewasz", "obrażona"], 1.2, "pl"),
                    (aiko.id, "talking", ["mów", "rozmawia", "powiedz", "odpowiedz", "pytam", "pytanie", "dlaczego", "jak", "co"], 0.8, "pl"),
                    
                    # English - Aiko
                    (aiko.id, "happy", ["joy", "laugh", "wonderful", "amazing", "great", "love", "thank you", "friend", "cute"], 1.0, "en"),
                    (aiko.id, "happy", ["haha", "lol", "xD", ":)", "😊", "😄"], 1.3, "en"),
                    (aiko.id, "sad", ["sad", "cry", "tears", "pain", "lonely", "loss", "sorry"], 1.1, "en"),
                    (aiko.id, "angry", ["angry", "furious", "hate", "terrible", "awful"], 1.0, "en"),
                    (aiko.id, "embarrassed", ["blush", "embarrassed", "shy", "awkward"], 1.2, "en"),
                    (aiko.id, "pouting", ["pout", "upset", "sulky", "mad"], 1.1, "en"),
                ]
                
                for char_id, emotion, keyword_list, weight, lang in keywords_data:
                    for keyword in keyword_list:
                        session.add(EmotionKeyword(
                            character_id=char_id,
                            emotion=emotion,
                            keyword=keyword,
                            weight=weight,
                            language=lang
                        ))
                
                session.commit()
                print("   ✅ Aiko keywords added")
         
        # ==================== 4. CONVERSATIONS ====================
        print("💬 Seeding Conversations...")
        
        conv1 = None
        conv2 = None
        
        if aiko.id is not None:
            conv1 = session.exec(
                select(Conversation).where(Conversation.character_id == aiko.id)
                .where(Conversation.message_count > 0)
            ).first()
            
            if not conv1:
                conv1 = Conversation(
                    character_id=aiko.id,
                    title="Pierwsza rozmowa z Aiko",
                    message_count=6,
                    is_active=True,
                    last_activity=datetime.now(timezone.utc) - timedelta(days=1)
                )
                session.add(conv1)
                session.commit()
                session.refresh(conv1)  
                
                conv2 = Conversation(
                    character_id=aiko.id,
                    title="Rozmowa o trudnym dniu",
                    message_count=4,
                    is_active=False,
                    last_activity=datetime.now(timezone.utc) - timedelta(days=2)
                )
                session.add(conv2)
                session.commit()
                session.refresh(conv2)  
                print("   ✅ Conversations created")
        
        # ==================== 5. MESSAGES ====================
        print("💭 Seeding Messages...")
        
        # Only create messages if conversations exist and have IDs
        if conv1 is not None and conv1.id is not None and conv2 is not None and conv2.id is not None:
            msg_count = session.exec(select(Message).where(Message.conversation_id == conv1.id)).first()
            
            if not msg_count:
                messages_conv1 = [
                    Message(
                        conversation_id=conv1.id,
                        role="user",
                        content="Cześć Aiko! Jak się masz?",
                        language="pl"
                    ),
                    Message(
                        conversation_id=conv1.id,
                        role="assistant",
                        content="Hej! Cudownie widzieć Cię znowu! 😊 Mam się świetnie, dziękuję za pytanie! A u Ciebie jak?",
                        emotion="happy",
                        emotion_confidence=0.85,
                        ai_detected_emotion="happy",
                        language="pl",
                        generation_time_ms=1250,
                        token_count=45
                    ),
                    Message(
                        conversation_id=conv1.id,
                        role="user",
                        content="U mnie super! Właśnie skończyłem projekt z Three.js!",
                        language="pl"
                    ),
                    Message(
                        conversation_id=conv1.id,
                        role="assistant",
                        content="O wow! Three.js to niesamowita biblioteka! Brawo! 🎉 Musiałeś się naprawdę napracować. Jestem z Ciebie taka dumna! Pokażesz mi kiedyś co stworzyłeś?",
                        emotion="happy",
                        emotion_confidence=0.92,
                        ai_detected_emotion="excited",
                        language="pl",
                        generation_time_ms=2100,
                        token_count=67
                    ),
                    Message(
                        conversation_id=conv1.id,
                        role="user",
                        content="Oczywiście! A co u Ciebie słychać? Co nowego?",
                        language="pl"
                    ),
                    Message(
                        conversation_id=conv1.id,
                        role="assistant",
                        content="U mnie wszystko po staremu... czekam na nasze rozmowy! To zawsze najlepsza część mojego dnia. *rumieni się lekko* Ale nie mów tego nikomu, okej?",
                        emotion="embarrassed",
                        emotion_confidence=0.78,
                        ai_detected_emotion="shy",
                        language="pl",
                        generation_time_ms=1800,
                        token_count=56
                    ),
                ]
                
                messages_conv2 = [
                    Message(
                        conversation_id=conv2.id,
                        role="user",
                        content="Aiko, mam dzisiaj bardzo zły dzień...",
                        language="pl"
                    ),
                    Message(
                        conversation_id=conv2.id,
                        role="assistant",
                        content="Och nie, to mnie smuci... Chcesz porozmawiać o tym? Jestem tu dla Ciebie. *delikatnie przytula*",
                        emotion="sad",
                        emotion_confidence=0.75,
                        ai_detected_emotion="concerned",
                        language="pl",
                        generation_time_ms=1400,
                        token_count=38
                    ),
                    Message(
                        conversation_id=conv2.id,
                        role="user",
                        content="Mój kot zachorował i jestem bardzo smutny...",
                        language="pl"
                    ),
                    Message(
                        conversation_id=conv2.id,
                        role="assistant",
                        content="Bardzo mi przykro... Wiem jak bardzo można kochać swojego futrzaka. Łzy same mi lecą na myśl o tym. Trzymaj się proszę. *płacze cicho*",
                        emotion="sad",
                        emotion_confidence=0.89,
                        ai_detected_emotion="crying",
                        language="pl",
                        generation_time_ms=1900,
                        token_count=51
                    ),
                ]
                
                for msg in messages_conv1 + messages_conv2:
                    session.add(msg)
                
                session.commit()
                print("   ✅ Messages created")
            
        # ==================== 6. EMOTION LOGS ====================
        print("📈 Seeding Emotion Logs...")
        
        if conv1 is not None and conv1.id is not None:
            log_count = session.exec(select(EmotionLog).where(EmotionLog.conversation_id == conv1.id)).first()
            if not log_count:
                emotion_logs = [
                    EmotionLog(
                        conversation_id=conv1.id,
                        message_id=2,  
                        emotion="happy",
                        confidence=0.85,
                        trigger_source="keyword"
                    ),
                    EmotionLog(
                        conversation_id=conv1.id,
                        message_id=4,
                        emotion="happy",
                        confidence=0.92,
                        trigger_source="keyword"
                    ),
                    EmotionLog(
                        conversation_id=conv1.id,
                        message_id=6,
                        emotion="embarrassed",
                        confidence=0.78,
                        trigger_source="keyword"
                    ),
                ]
                
                for log in emotion_logs:
                    session.add(log)
                
                session.commit()
                print("   ✅ Emotion logs created")
                
        # ==================== 7. VRM MODEL CACHE ====================
        print("🎨 Seeding VRM Model Cache...")
        
        cache_count = session.exec(select(VRMModelCache)).first()
        if not cache_count:
            vrm_models = [
                VRMModelCache(
                    file_path="/models/aiko.vrm",
                    file_hash=get_file_hash("/models/aiko.vrm"),
                    file_size=15485760,  # ~15MB
                    vrm_version="1.0",
                    thumbnail_path="/thumbnails/aiko.png",
                    blendshape_count=32,
                    blendshape_names='["neutral", "joy", "angry", "sorrow", "fun", "surprised", "aa", "ih", "ou", "ee", "oh", "blink", "blinkLeft", "blinkRight", "lookUp", "lookDown", "lookLeft", "lookRight"]',
                    load_time_ms=2300,
                    use_count=42
                ),
                VRMModelCache(
                    file_path="/models/kaito.vrm",
                    file_hash=get_file_hash("/models/kaito.vrm"),
                    file_size=18954240,  # ~18MB
                    vrm_version="1.0",
                    thumbnail_path="/thumbnails/kaito.png",
                    blendshape_count=28,
                    blendshape_names='["neutral", "joy", "angry", "sorrow", "blink", "lookUp", "lookDown", "aa", "ih", "ou"]',
                    load_time_ms=3100,
                    use_count=7
                ),
                VRMModelCache(
                    file_path="/models/sakura.vrm",
                    file_hash=get_file_hash("/models/sakura.vrm"),
                    file_size=22118400,  # ~22MB
                    vrm_version="1.0",
                    thumbnail_path="/thumbnails/sakura.png",
                    blendshape_count=45,
                    blendshape_names='["neutral", "joy", "angry", "sorrow", "fun", "surprised", "aa", "ih", "ou", "ee", "oh", "blink", "blinkLeft", "blinkRight", "lookUp", "lookDown", "lookLeft", "lookRight", "a", "i", "u", "e", "o"]',
                    load_time_ms=2850,
                    use_count=15
                ),
            ]
            
            for model in vrm_models:
                session.add(model)
            
            session.commit()
            print("   ✅ VRM cache created")

        print("✅ Database seeding complete!")
        
        # ==================== STATS ====================
        stats = {
            "characters": session.exec(select(Character)).all(),
            "conversations": session.exec(select(Conversation)).all(),
            "messages": session.exec(select(Message)).all(),
            "keywords": session.exec(select(EmotionKeyword)).all(),
            "vrm_models": session.exec(select(VRMModelCache)).all(),
        }
        
        print("\n📊 Database Stats:")
        for key, items in stats.items():
            print(f"   {key.capitalize()}: {len(items)}")
        

if __name__ == "__main__":
    seed_database()
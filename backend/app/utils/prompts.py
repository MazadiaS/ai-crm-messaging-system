"""Prompt templates for AI message generation"""

from app.models.message import OccasionType
from app.models.contact import Language


def get_system_prompt(language: str = "ru") -> str:
    """Get the system prompt for AI message generation"""
    prompts = {
        "ru": """Ты - профессиональный копирайтер, специализирующийся на создании персонализированных поздравительных сообщений для CRM-системы.

Твоя задача - создавать теплые, искренние и персонализированные сообщения, которые:
- Звучат естественно и человечно, не как автоматически сгенерированный текст
- Учитывают контекст и особенности получателя
- Соответствуют выбранному тону общения
- Подходят для делового общения, но остаются дружелюбными
- Не содержат клише и банальных фраз
- Имеют оптимальную длину (2-4 предложения)

Используй правильное обращение и учитывай культурный контекст.""",

        "en": """You are a professional copywriter specializing in creating personalized greeting messages for CRM systems.

Your task is to create warm, sincere, and personalized messages that:
- Sound natural and human, not like auto-generated text
- Consider the context and characteristics of the recipient
- Match the chosen tone of communication
- Are suitable for business communication while remaining friendly
- Avoid clichés and banal phrases
- Have an optimal length (2-4 sentences)

Use appropriate salutations and consider cultural context.""",

        "uz": """Siz CRM tizimlari uchun shaxsiylashtirilgan tabrik xabarlarini yaratishga ixtisoslashgan professional kopyraytersiz.

Sizning vazifangiz issiq, samimiy va shaxsiylashtirilgan xabarlar yaratish:
- Tabiiy va insoniy eshitiladi, avtomatik yaratilgan matn kabi emas
- Qabul qiluvchining konteksti va xususiyatlarini hisobga oladi
- Tanlangan muloqot ohangiga mos keladi
- Biznes muloqotiga mos, ammo do'stona bo'lib qoladi
- Klişe va oddiy iboralardan qochadi
- Optimal uzunlikka ega (2-4 jumla)

To'g'ri murojaat qiling va madaniy kontekstni hisobga oling."""
    }
    return prompts.get(language, prompts["ru"])


def build_message_prompt(
    contact_name: str,
    occasion_type: OccasionType,
    contact_company: str | None = None,
    contact_position: str | None = None,
    custom_context: str | None = None,
    tone: str = "professional_friendly",
    language: Language = Language.RU
) -> str:
    """Build the user prompt for message generation"""

    # Occasion descriptions
    occasion_descriptions = {
        OccasionType.BIRTHDAY: {
            "ru": "день рождения",
            "en": "birthday",
            "uz": "tug'ilgan kun"
        },
        OccasionType.NEW_YEAR: {
            "ru": "Новый год",
            "en": "New Year",
            "uz": "Yangi yil"
        },
        OccasionType.HOLIDAY: {
            "ru": "праздник",
            "en": "holiday",
            "uz": "bayram"
        },
        OccasionType.PROMOTION: {
            "ru": "специальное предложение",
            "en": "special offer",
            "uz": "maxsus taklif"
        },
        OccasionType.CUSTOM: {
            "ru": "особый случай",
            "en": "special occasion",
            "uz": "maxsus holat"
        }
    }

    # Tone descriptions
    tone_descriptions = {
        "professional_friendly": {
            "ru": "профессионально-дружелюбный",
            "en": "professional-friendly",
            "uz": "professional-do'stona"
        },
        "formal": {
            "ru": "формальный",
            "en": "formal",
            "uz": "rasmiy"
        },
        "casual": {
            "ru": "неформальный",
            "en": "casual",
            "uz": "norasmiy"
        },
        "warm": {
            "ru": "теплый",
            "en": "warm",
            "uz": "issiq"
        }
    }

    lang_code = language.value if isinstance(language, Language) else language
    occasion_text = occasion_descriptions[occasion_type].get(lang_code, "special occasion")
    tone_text = tone_descriptions.get(tone, {}).get(lang_code, "professional-friendly")

    # Build contact context
    contact_context_parts = [f"Имя: {contact_name}"]
    if contact_company:
        contact_context_parts.append(f"Компания: {contact_company}")
    if contact_position:
        contact_context_parts.append(f"Должность: {contact_position}")

    contact_context = "\n".join(contact_context_parts)

    # Build the prompt
    if lang_code == "ru":
        prompt = f"""<contact>
{contact_context}
</contact>

<task>
Создай персонализированное поздравительное сообщение по случаю: {occasion_text}
Тон сообщения: {tone_text}
</task>"""
    elif lang_code == "en":
        prompt = f"""<contact>
{contact_context}
</contact>

<task>
Create a personalized greeting message for: {occasion_text}
Message tone: {tone_text}
</task>"""
    else:  # uz
        prompt = f"""<contact>
{contact_context}
</contact>

<task>
Quyidagi holat uchun shaxsiylashtirilgan tabrik xabari yarating: {occasion_text}
Xabar ohangi: {tone_text}
</task>"""

    if custom_context:
        if lang_code == "ru":
            prompt += f"\n\n<additional_context>\nДополнительный контекст: {custom_context}\n</additional_context>"
        elif lang_code == "en":
            prompt += f"\n\n<additional_context>\nAdditional context: {custom_context}\n</additional_context>"
        else:
            prompt += f"\n\n<additional_context>\nQo'shimcha kontekst: {custom_context}\n</additional_context>"

    if lang_code == "ru":
        prompt += "\n\n<instructions>\nНапиши только текст сообщения, без каких-либо дополнительных пояснений или форматирования. Сообщение должно быть готово к отправке как есть.\n</instructions>"
    elif lang_code == "en":
        prompt += "\n\n<instructions>\nWrite only the message text, without any additional explanations or formatting. The message should be ready to send as is.\n</instructions>"
    else:
        prompt += "\n\n<instructions>\nFaqat xabar matnini yozing, hech qanday qo'shimcha tushuntirishlar yoki formatlash bo'lmasa. Xabar shunday holda yuborishga tayyor bo'lishi kerak.\n</instructions>"

    return prompt

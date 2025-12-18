"""AI message generation service using OpenAI API"""

from openai import OpenAI
from typing import Dict, Any, List
from datetime import datetime

from app.config.settings import settings
from app.models.contact import Contact
from app.models.message import OccasionType
from app.utils.prompts import get_system_prompt, build_message_prompt


class AIMessageGenerator:
    """Service for generating personalized messages using OpenAI"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_AI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.AI_TEMPERATURE

    def generate_personalized_message(
        self,
        contact: Contact,
        occasion_type: OccasionType,
        custom_context: str | None = None,
        tone: str = "professional_friendly",
    ) -> Dict[str, Any]:
        """
        Generate a personalized message for a contact

        Args:
            contact: Contact object
            occasion_type: Type of occasion
            custom_context: Additional context for generation
            tone: Desired tone of the message

        Returns:
            Dictionary with generated message and metadata
        """
        try:
            # Build prompts
            system_prompt = get_system_prompt(contact.language.value)
            user_prompt = build_message_prompt(
                contact_name=contact.name,
                occasion_type=occasion_type,
                contact_company=contact.company,
                contact_position=contact.position,
                custom_context=custom_context,
                tone=tone,
                language=contact.language
            )

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract message content
            message_content = response.choices[0].message.content.strip()

            # Calculate cost estimate (approximate)
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Approximate costs (USD per 1M tokens) for GPT-4o
            # GPT-4o: $2.50 input, $10.00 output (as of 2024)
            input_cost = (input_tokens / 1_000_000) * 2.5
            output_cost = (output_tokens / 1_000_000) * 10.0
            total_cost = input_cost + output_cost

            # Build metadata
            metadata = {
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "cost_usd": round(total_cost, 6),
                "tone": tone,
                "language": contact.language.value,
                "generated_at": datetime.utcnow().isoformat(),
                "occasion_type": occasion_type.value,
            }

            return {
                "success": True,
                "content": message_content,
                "metadata": metadata,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "metadata": {"error_type": "api_error"},
                "error": f"OpenAI API error: {str(e)}"
            }

    def batch_generate(
        self,
        contacts: List[Contact],
        occasion_type: OccasionType,
        custom_context: str | None = None,
        tone: str = "professional_friendly",
    ) -> List[Dict[str, Any]]:
        """
        Generate messages for multiple contacts

        Args:
            contacts: List of Contact objects
            occasion_type: Type of occasion
            custom_context: Additional context for generation
            tone: Desired tone of the message

        Returns:
            List of dictionaries with results for each contact
        """
        results = []

        for contact in contacts:
            result = self.generate_personalized_message(
                contact=contact,
                occasion_type=occasion_type,
                custom_context=custom_context,
                tone=tone
            )

            results.append({
                "contact_id": str(contact.id),
                "contact_name": contact.name,
                **result
            })

        return results

    def get_fallback_message(
        self,
        contact_name: str,
        occasion_type: OccasionType,
        language: str = "ru"
    ) -> str:
        """
        Get a fallback message when AI generation fails

        Args:
            contact_name: Name of the contact
            occasion_type: Type of occasion
            language: Language code

        Returns:
            Generic fallback message
        """
        fallback_messages = {
            "ru": {
                OccasionType.BIRTHDAY: f"Уважаемый(ая) {contact_name}! Поздравляем Вас с Днем рождения! Желаем успехов, здоровья и процветания!",
                OccasionType.NEW_YEAR: f"Уважаемый(ая) {contact_name}! Поздравляем Вас с Новым годом! Желаем успехов в новом году!",
                OccasionType.HOLIDAY: f"Уважаемый(ая) {contact_name}! Поздравляем Вас с праздником!",
                OccasionType.PROMOTION: f"Уважаемый(ая) {contact_name}! У нас для Вас специальное предложение!",
                OccasionType.CUSTOM: f"Уважаемый(ая) {contact_name}! Благодарим за сотрудничество!",
            },
            "en": {
                OccasionType.BIRTHDAY: f"Dear {contact_name}! Happy Birthday! Wishing you success, health and prosperity!",
                OccasionType.NEW_YEAR: f"Dear {contact_name}! Happy New Year! Wishing you success in the new year!",
                OccasionType.HOLIDAY: f"Dear {contact_name}! Happy holidays!",
                OccasionType.PROMOTION: f"Dear {contact_name}! We have a special offer for you!",
                OccasionType.CUSTOM: f"Dear {contact_name}! Thank you for your partnership!",
            },
            "uz": {
                OccasionType.BIRTHDAY: f"Hurmatli {contact_name}! Tug'ilgan kuningiz bilan! Sizga omad, sog'lik va farovonlik tilaymiz!",
                OccasionType.NEW_YEAR: f"Hurmatli {contact_name}! Yangi yilingiz bilan! Yangi yilda muvaffaqiyatlar tilaymiz!",
                OccasionType.HOLIDAY: f"Hurmatli {contact_name}! Bayramingiz bilan!",
                OccasionType.PROMOTION: f"Hurmatli {contact_name}! Siz uchun maxsus taklifimiz bor!",
                OccasionType.CUSTOM: f"Hurmatli {contact_name}! Hamkorlik uchun rahmat!",
            }
        }

        return fallback_messages.get(language, fallback_messages["ru"]).get(
            occasion_type,
            f"Dear {contact_name}! Thank you for your partnership!"
        )


# Singleton instance
ai_generator = AIMessageGenerator()

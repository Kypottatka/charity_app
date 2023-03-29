from main.models import FundraisingCampaign, Comment

# Создайте или получите объект FundraisingCampaign
fundraising_campaign = FundraisingCampaign.objects.first()
"""
# Создайте комментарий, связанный с этим объектом
comment = Comment(
    user=user,
    content="Отличная кампания!",
    content_type=ContentType.objects.get_for_model(FundraisingCampaign),
    object_id=fundraising_campaign.id
)
comment.save()
"""
from django.db import models

from users.models import User


class PhotoCard(models.Model):
    ALBUM = "album"
    SPECIAL_GIFT = "special_gift"
    FAN_SIGNING_EVENT = "fan_signing_event"
    SEASON_GREETING = "season_greeting"
    FAN_MEETING = "fan_meeting"
    CONCERT = "concert"
    MD = "md"
    COLLABORATION = "collaboration"
    FAN_CLUB = "fan_club"
    ETC = "etc"
    RELEASE_TYPE_CHOICES = {
        ALBUM: "앨범",
        SPECIAL_GIFT: "특전",
        FAN_SIGNING_EVENT: "팬싸",
        SEASON_GREETING: "시즌그리팅",
        FAN_MEETING: "팬미팅",
        CONCERT: "콘서트",
        MD: "MD",
        COLLABORATION: "콜라보",
        FAN_CLUB: "팬클럽",
        ETC: "기타",
    }

    title = models.CharField(max_length=255)
    release_type = models.CharField(max_length=50, choices=RELEASE_TYPE_CHOICES)
    group_name = models.CharField("아이돌 그룹 명", max_length=255)
    member_name = models.CharField("멤버 명", max_length=255)
    release_date = models.DateField("발매 날짜", null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class RegisteredPhotoCard(models.Model):
    AVAILABLE = "available"
    SOLD = "sold"
    DELETED = "deleted"
    STATE_CHOICES = {
        AVAILABLE: "판매중",
        SOLD: "판매완료",
        DELETED: "삭제",
    }
    
    photo_card = models.ForeignKey(
        PhotoCard, 
        on_delete=models.RESTRICT, 
        related_name="photo_card"
    )
    price = models.PositiveIntegerField("가격")
    fee = models.PositiveIntegerField("수수료")
    state = models.CharField(
        "판매 상태", 
        choices=STATE_CHOICES, 
        max_length=50, 
        default="available"
    )
    buyer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        related_name="purchased_photo_cards"
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="sold_photo_cards"
    )
    create_date = models.DateTimeField("등록 날짜", auto_now_add=True)
    update_date = models.DateTimeField("수정 날짜", auto_now=True)
    renewal_date = models.DateTimeField("가격 수정 날짜", auto_now_add=True)
    sold_date = models.DateTimeField("판매 날짜", null=True)

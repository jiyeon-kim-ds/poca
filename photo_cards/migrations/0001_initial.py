# Generated by Django 5.1 on 2024-08-24 07:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PhotoCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "release_type",
                    models.CharField(
                        choices=[
                            ("album", "앨범"),
                            ("special_gift", "특전"),
                            ("fan_signing_event", "팬싸"),
                            ("season_greeting", "시즌그리팅"),
                            ("fan_meeting", "팬미팅"),
                            ("concert", "콘서트"),
                            ("md", "MD"),
                            ("collaboration", "콜라보"),
                            ("fan_club", "팬클럽"),
                            ("etc", "기타"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "group_name",
                    models.CharField(max_length=255, verbose_name="아이돌 그룹 명"),
                ),
                ("member_name", models.CharField(max_length=255, verbose_name="멤버 명")),
                ("release_date", models.DateField(null=True, verbose_name="발매 날짜")),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="RegisteredPhotoCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.PositiveIntegerField(verbose_name="가격")),
                ("fee", models.PositiveIntegerField(verbose_name="수수료")),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("available", "판매중"),
                            ("sold", "판매완료"),
                            ("deleted", "삭제"),
                        ],
                        default="available",
                        max_length=50,
                        verbose_name="판매 상태",
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="등록 날짜"),
                ),
                (
                    "update_date",
                    models.DateTimeField(auto_now=True, verbose_name="수정 날짜"),
                ),
                (
                    "renewal_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="가격 수정 날짜"),
                ),
                ("sold_date", models.DateTimeField(null=True, verbose_name="판매 날짜")),
                (
                    "buyer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="purchased_photo_cards",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "photo_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="photo_card",
                        to="photo_cards.photocard",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="sold_photo_cards",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

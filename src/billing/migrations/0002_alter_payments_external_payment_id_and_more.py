# Generated by Django 5.0 on 2024-02-02 10:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payments",
            name="external_payment_id",
            field=models.CharField(unique=True, verbose_name="external_payment_id"),
        ),
        migrations.AlterField(
            model_name="payments",
            name="status",
            field=models.CharField(
                choices=[
                    ("need_confirm", "Need Confirm"),
                    ("succeeded", "Succeeded"),
                    ("canceled", "Canceled"),
                    ("pending", "Pending"),
                    ("error", "Error"),
                ],
                default="pending",
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="refunds",
            name="amount",
            field=models.FloatField(blank=True, null=True, verbose_name="amount"),
        ),
        migrations.AlterField(
            model_name="refunds",
            name="currency",
            field=models.CharField(
                choices=[("RUB", "Rub"), ("USD", "Usd"), ("EUR", "Eur")], default="RUB", verbose_name="currency"
            ),
        ),
        migrations.AlterField(
            model_name="refunds",
            name="external_refund_id",
            field=models.CharField(blank=True, unique=True, verbose_name="external_refund_id"),
        ),
        migrations.AlterField(
            model_name="refunds",
            name="status",
            field=models.CharField(
                choices=[
                    ("need_confirm", "Need Confirm"),
                    ("succeeded", "Succeeded"),
                    ("canceled", "Canceled"),
                    ("pending", "Pending"),
                    ("error", "Error"),
                ],
                default="need_confirm",
                verbose_name="status",
            ),
        ),
    ]

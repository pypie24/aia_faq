import json
import asyncio
import logging

import typer

from src.db import AsyncSessionLocal, bulk_insert_ignore_conflicts
from src.models.product_models import (
    Brand,
    Category,
    ProductLines,
    Product,
    ProductVariant,
    Tag,
    ProductVariantTag,
)
from src.tasks.embedding_tasks import process_unembedding_queue


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
cli = typer.Typer()


@cli.command()
def populatedb():
    brand_data = []
    category_data = []
    product_data = []
    product_lines_data = []
    product_variant_data = []
    tag_data = []
    product_variant_tag_data = []

    with open("sample_data/brands.json", "r") as brand_file:
        brand_data = json.load(brand_file)

    with open("sample_data/categories.json", "r") as categories_file:
        category_data = json.load(categories_file)

    with open("sample_data/products.json", "r") as products_file:
        product_data = json.load(products_file)

    with open("sample_data/product_lines.json", "r") as product_lines_file:
        product_lines_data = json.load(product_lines_file)

    with open("sample_data/product_variants.json", "r") as product_variants_file:
        product_variant_data = json.load(product_variants_file)

    with open("sample_data/tags.json", "r") as tags_file:
        tag_data = json.load(tags_file)

    with open("sample_data/product_variants_tags.json", "r") as product_variant_tags_file:
        product_variant_tag_data = json.load(product_variant_tags_file)

    async def populate_db():
        async with AsyncSessionLocal() as db:
            log.info("Populating database...")

            log.info("Inserting Brands...")
            await bulk_insert_ignore_conflicts(
                db,
                Brand,
                brand_data,
                ["name"]
            )
            log.info("Done Inserting Brands...")

            log.info("Inserting Categories...")
            await bulk_insert_ignore_conflicts(
                db,
                Category,
                category_data,
                ["name"]
            )
            log.info("Done Inserting Categories...")

            log.info("Inserting Tags...")
            await bulk_insert_ignore_conflicts(
                db,
                Tag,
                tag_data,
                ["name"]
            )
            log.info("Done Inserting Tags...")

            log.info("Inserting Product Lines...")
            await bulk_insert_ignore_conflicts(
                db,
                ProductLines,
                product_lines_data,
                ["name", "brand_id", "category_id"]
            )
            log.info("Done Inserting Product Lines...")

            log.info("Inserting Products...")
            await bulk_insert_ignore_conflicts(
                db,
                Product,
                product_data,
                ["name", "product_line_id"]
            )
            log.info("Done Inserting Products...")

            log.info("Inserting Product Variants...")
            await bulk_insert_ignore_conflicts(
                db,
                ProductVariant,
                product_variant_data,
                ["name", "product_id"]
            )
            log.info("Done Inserting Product Variants...")

            log.info("Inserting Product Variant Tags...")
            await bulk_insert_ignore_conflicts(
                db,
                ProductVariantTag,
                product_variant_tag_data,
                ["variant_id", "tag_id"]
            )
            log.info("Done Inserting Product Variant Tags...")

    asyncio.run(populate_db())


@cli.command()
def embeddingdb():
    log.info("Processing unembedding queue...")
    process_unembedding_queue()
    log.info("Unembedding queue processed.")


if __name__ == "__main__":
    cli()

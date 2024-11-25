import argparse
import asyncio
import logging
from aiopath import AsyncPath
import aioshutil

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def read_folder(source: AsyncPath, output: AsyncPath):
    if not await source.exists():
        logging.error(f"Source folder {source} does not exist.")
        return

    tasks = []
    async for item in source.rglob("*"):
        if await item.is_file():
            tasks.append(copy_file(item, output))

    await asyncio.gather(*tasks)


async def copy_file(path: AsyncPath, output_folder: AsyncPath):
    extension = path.suffix.lower()
    target_folder = output_folder / (
        extension.lstrip(".") if extension else "no_extension"
    )

    try:
        await target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / path.name

        await aioshutil.copy(path, target_path)
        logging.info(f"Copied {path} to {target_path}")
    except Exception as e:
        logging.error(f"Error copying file {path}: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="File sorting")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to the source folder.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output folder.",
    )
    return parser.parse_args()


async def main():
    args = parse_arguments()
    source_folder = AsyncPath(args.source)
    output_folder = AsyncPath(args.output)

    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    asyncio.run(main())

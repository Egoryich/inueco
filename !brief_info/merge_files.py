import os
import argparse

def should_ignore(path, ignore_dirs=None):
    """Проверка, нужно ли игнорировать директорию"""
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', '.idea']
    return any(ignore_dir in path.split(os.sep) for ignore_dir in ignore_dirs)

def process_directory(root_path, current_path, output_file, level=1, section_prefix="", ignore_dirs=None):
    """Рекурсивная обработка директории"""
    try:
        entries = sorted(os.listdir(current_path))
    except PermissionError:
        return

    # Сначала обрабатываем файлы
    for entry in entries:
        entry_path = os.path.join(current_path, entry)
        if os.path.isfile(entry_path):
            try:
                with open(entry_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
            except (UnicodeDecodeError, PermissionError):
                continue
            
            filename = os.path.basename(entry_path)
            output_file.write(f"{filename}\n{content}\n\n")

    # Затем обрабатываем поддиректории
    for entry in entries:
        entry_path = os.path.join(current_path, entry)
        if os.path.isdir(entry_path) and not should_ignore(entry_path, ignore_dirs):
            section_name = os.path.basename(entry_path)
            new_prefix = f"{section_prefix}{level}."
            
            # Записываем заголовок раздела
            output_file.write(f"{new_prefix} {section_name}\n\n")
            
            # Рекурсивно обрабатываем вложенную директорию
            process_directory(
                root_path,
                entry_path,
                output_file,
                level + 1,
                new_prefix,
                ignore_dirs
            )

def main():
    parser = argparse.ArgumentParser(description='Объединение текстовых файлов в структурированный документ')
    parser.add_argument('input_dir', help='Путь к исходной директории')
    parser.add_argument('output_file', help='Путь к выходному файлу')
    parser.add_argument('--ignore', nargs='+', help='Директории для игнорирования', default=['.git', '__pycache__'])
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Ошибка: Директория {args.input_dir} не существует")
        return

    with open(args.output_file, 'w', encoding='utf-8') as output_file:
        process_directory(
            args.input_dir,
            args.input_dir,
            output_file,
            ignore_dirs=args.ignore
        )

    print(f"Файлы успешно объединены в {args.output_file}")

if __name__ == "__main__":
    main()
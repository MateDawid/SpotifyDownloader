from FileChecker import FileChecker


if __name__ == '__main__':
    file_checker = FileChecker()
    file_checker.set_directory('E:\[MUZYKA]\WSZYSTKIE')
    file_checker.get_downloaded_playlist()
    file_checker.print_downloaded_playlist()
import os


# Чтобы не творить хаос в основной директории, все txt файлы были помещены в директорию Module_7_3_files
# Логика несколько изменена. В объект передаются папки, а файлы уже ищутся сами
# UPDT. Логика расширена: класс принимает папки и названия фалов (из основной директории)
# Таким образом полностью выполняются условия основного задания

class WordsFinder:
    def __init__(self, *args):
        self.folders = []
        self.files = []
        # Далее распределяем файлы и папки по двум спискам
        for arg in args:
            if arg.endswith('.txt'):
                self.files.append(arg)
            else:
                self.folders.append(arg)
        self.all_words = {}
        pass

    def get_all_words(self):
        for folder in self.folders:
            if os.path.isdir(folder):  # Проверка на существование каталога
                files_list = os.listdir(folder)  # Делаем список файлов в директории
                for i in range(len(files_list)):
                    files_list[i] = os.path.join(folder, files_list[i])  # Соединяем название файла с директорией
                files_list.extend(self.files)  # Соединяем со списком файлов в основной директории
                files_list = set(files_list)  # Убираем дубли, если есть
                # После всего получаем единый кортеж типа 'директория\файл' или 'файл' (если в основной папке)
                # И то, и другое пригодно для передачи в функцию open в текущем виде (для этого все и делалось)
                self.__find_in(files_list)  # Для поиска и обработки слов написана отдельная служебная функция __find_in
        return self.all_words

    def __find_in(self, fnd_lst):
        punct = [',', '.', '=', '!', '?', ';', ':', '— ', ' -', '\"']
        for file_txt in fnd_lst:
            if os.path.isfile(file_txt):  # Проверка на существование файла
                with open(file_txt, 'r', encoding='utf-8') as file:
                    lines = file.readlines()  # Считываем все строки в список и закрываем файл
                words = []
                for line in lines:
                    line = line.strip().casefold()  # Убираем символы переноса и пробелы по бокам, делаем нижний регистр
                    for sign in punct:  # Удаляем различные символы
                        line = line.replace(sign, '')
                    for word in line.split():
                        words.append(word)
                self.all_words[file_txt] = words

    def find(self, word):
        found = {}
        print(f'Результаты поиска по слову: {word}')
        word = word.casefold()
        self.get_all_words()
        for key, word_list in self.all_words.items():
            if word in word_list:
                found[key] = word_list.index(word)
        if found:
            self.print_all(found, method='Find')
        else:
            print(f'Слово "{word}" не найдено')

    def count(self, word):
        count = {}
        print(f'Результаты подсчета по слову: {word}')
        word = word.casefold()
        self.get_all_words()
        for key, word_list in self.all_words.items():
            if word in word_list:
                count[key] = word_list.count(word)
        if count:
            self.print_all(count, method='Count')
        else:
            print(f'Слово "{word}" не найдено')

    def print_all(self, any_dict=None, *, method='Index\\count'):
        # Ввели переменную method, чтобы выводить результаты с подписью конкретного метода
        if any_dict is None:
            any_dict = self.all_words
        for file, words in any_dict.items():
            print(f'File: {os.path.split(file)[1]}')
            print(f'Path: \\{os.path.split(file)[0]}') if os.path.split(file)[0] else print('Path: MAIN DIR')
            if any_dict == self.all_words:  # Вариативность печати в зависимости от словаря
                print(f'Words: {words}') if words else print('No words')
            else:
                print(f'{method}: {words}')  # Для метода find и count
            print()


# Для проверки работы всех ф-ций класса, вводим существующие и несуществующие папки и файлы
finder = WordsFinder('Module_7_3_files', 'Module_7_3_morefiles', 'text_main.txt', 'no_catalog', 'no_file.txt',
                     'no_file.exe')
finder.get_all_words()
finder.print_all()
print()
# Объявим новые переменные класса WordsFinder (чистые) и воспользуемся методами find и count
finder2 = WordsFinder('Module_7_3_files', 'Module_7_3_morefiles', 'text_main.txt', 'no_catalog', 'no_file.txt',
                      'no_file.exe')
print('Ищем слово: my')
finder2.find('my')
finder2.find('сТУЛ')
print()
print('Считаем слово: text (разное написание)')
finder3 = WordsFinder('Module_7_3_files', 'Module_7_3_morefiles', 'text_main.txt', 'no_catalog', 'no_file.txt',
                      'no_file.exe')
finder3.count('TEXT')
finder3.count('TExt')
finder3.count('fortuna')

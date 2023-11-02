import argparse
import requests

def main():
    try:
        # Create a simple parser to parse arguments from a command line.
        parser = argparse.ArgumentParser(
            prog="freectionary.py",
            description='''Get the word definition. 
            Words should be supplied in a file, separated by a newline.'''
        )
        parser.add_argument(
            'wordlist',
            metavar='wordlist',
            type=str,
            help='Path to a wordlist file.'
        )
        args = parser.parse_args()

        # Create a variable with a path to the file.
        wordlist = args.wordlist

        # Read a list of words to check in the dictionary.
        words = []
        with open(wordlist, 'r', encoding='UTF-8') as f:
            for word in f.read().splitlines():
                words.append(word)

        # Check the words in the Free Dictionary API.
        # And we also create a dictionary of words and meanings.
        meaning_dictionary = {}
        for word in words:
            definition_counter = 1
            try:
                meaning = ''
                r = requests.get(
                    f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
                )
                # Get the first definition.
                response_dictionary = r.json()[0]
                meanings = response_dictionary['meanings']
                for element in meanings:
                    definitions = element['definitions']
                    for definition in definitions:
                        meaning += str(definition_counter) + '. ' + (definition['definition']) + '\n'
                        definition_counter += 1
                meaning_dictionary[word] = meaning
            except Exception as e:
                pass

        # And now... return the dictionary in a Markdown-friendly manner.
        # And write it into a file.
        for word in meaning_dictionary:
            entry = f'***{word}***\n' + meaning_dictionary[word]
            print(entry)
            with open('dictionary.txt', 'a', encoding="UTF-8") as f:
                f.write(entry)
                f.write("\n")
    except Exception as e:
        print(e)
main()
"""
MIT License

Copyright (c) 2023 tofh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


#----------------------------------------------------

# Author: tofh
# Last Updated: 12-08-2023
# Description: Response parser for xonstatus

#----------------------------------------------------

class token:
    """
    Token object, has a token type and a value
        token(type, value)
    """
    # All the supported token
    TT_GAMENAME = 'gamename'
    TT_MODNAME = 'modname'
    TT_GVERSION = 'gameversion'
    TT_MXCLIENTS = 'sv_maxclients'
    TT_CLIENTS = 'clients'
    TT_BOTS = 'bots'
    TT_MAPNAME = 'mapname'
    TT_HOSTNAME = 'hostname'
    TT_PROTO = 'protocol'
    TT_GMOD = 'gamemode'
    TT_QCSTATUS = 'qcstatus'
    TT_d0BINDID = 'd0_blind_id'
    TT_PLAYERS = 'players'

    def __init__(self, type, value):
        self.type = type  # token type
        self.value = value  # token value

    def __str__(self):
        return f"token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()



class Parser:
    """
    Parser for parsing xonstatus response, takes raw response as input
    """
    def __init__(self, response):
        self.response = response.decode("utf-8", "backslashreplace")  # Keeps the response
        self.pointer = 0
        self.tokens = []  # stores all the tokens

        ## SOME FORMATING OPTIONS
        self.remove_colors = False  # Remove player nick colors

    def parse(self):
        """
        Pasrse the response into a status dictionary
        """
        self.lexer()
        return self.status_constructor()

    def lexer(self):
        # First removing "\xff\xff\xff\xffstatusResponse" from the response
        response = self.response.replace("\\xff\\xff\\xff\\xffstatusResponse\n", "")
        while True:
            if self.pointer > len(response) - 1:
                break
            else:
                current_char = response[self.pointer]
                if current_char == "\\":
                    self.pointer += 1
                    word = self.make_word(response)
                    self.pointer += 1
                    if word == token.TT_GAMENAME:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_MODNAME:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_GVERSION:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_MXCLIENTS:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_CLIENTS:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_BOTS:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_MAPNAME:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_HOSTNAME:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_PROTO:
                        value = self.make_word(response)
                        self.tokens.append(token(word, value))

                    elif word == token.TT_QCSTATUS:
                        value = self.make_word(response)
                        self.tokens.append(token(token.TT_GMOD, value.split(":")[0]))
                        self.tokens.append(token(word, value))

                    elif word == token.TT_d0BINDID:
                        value = self.make_word(response, delimiter="\n")
                        self.tokens.append(token(word, value))
                        self.pointer += 1
                        if self.pointer == len(response):
                            self.tokens.append(token(token.TT_PLAYERS, None))
                        else:
                            self.tokens.append(token(token.TT_PLAYERS, response[self.pointer:]))
                else:
                    self.pointer += 1
        return self.tokens

    def make_word(self, response, delimiter='\\'):
        """
        Makes a word, until it hits a delimiter
        """
        word = ""
        while True:
            if self.pointer > len(response) - 1:
                break
            else:
                current_char = response[self.pointer]
                if current_char == delimiter:
                    break
                else:
                    word += current_char
                    self.pointer += 1
        return word

    def status_constructor(self):
        """
        Formats the tokens list to dictionary output
        """
        status = {}
        for tkn in self.tokens:
            if tkn.type == token.TT_PLAYERS and tkn.value is not None:
                status[tkn.type] = self.format_player_data(tkn.value)
            else:
                status[tkn.type] = tkn.value
        return status

    def format_player_data(self, data):
        """
        Format player data into proper dict structure
        """
        players = []
        if self.remove_colors:
            data = self.xonfilter(data)
        data = data.removesuffix("\n").split("\n")
        for player in data:
            status = player.split('"', 1)
            info = status[0].split()
            player_nick = status[1].removesuffix('"')
            if len(info) == 3:
                players.append(dict(score=info[0], ping=info[1], team=info[2], nick=player_nick))
            else:
                player.append(dict(score=info[0], ping=info[1], team=None, nick=player_nick))
        return players

    def xonfilter(self, c):
        """
        Remove Xon color codes from input string.
        """
        text = ""
        pointer = 0

        # looping through the input string
        while True:
            # if pointer exceeds the length of the input string, exit the loop
            if pointer > len(c) -1:
                break
            # else, get a character from the input string using pointer as index
            else:
                current_char = c[pointer]
                # if current char is carat "^", look if it's the last entry of the input text
                # meaning if current char is carat and pointer is equal to the input string length
                # add the current char to the text string and exit the loop
                if current_char == "^":
                    if pointer == len(c)-1:
                        text += current_char
                        break
                    # else, if the char at the next index is a digit, then it's a single digit color code
                    # advance the pointer 2 steps
                    elif c[pointer+1].isdigit():
                        pointer +=2
                    # else, if the char at the next index to the carat is "x" which indicates it's a hex color code
                    # extract the color code from the string at that index
                    elif c[pointer+1] == "x":
                        color = c[pointer+2:pointer+5]
                        # if the length of the extracted color code is 3 check if it's a valid hex value
                        # if true advance pointer 5 steps
                        if len(color) == 3:
                            try:
                                if int(color, 16) < 4096:
                                    pointer += 5
                            # if there is an error, mainly due to color not being a valid hex value
                            # add current char to the text string, advance pointer 1 step
                            except:
                                text += current_char
                                pointer += 1
                        # if the length of the color code is not 3 then add it to text string, advance pointer 1 step
                        else:
                            text += current_char
                            pointer += 1
                    # if the char next to ^ isn't any color code indicator add current char to text, advance pointer 1 step
                    else:
                        text += current_char
                        pointer += 1
                # if current char is not ^ add it to text, advance pointer 1 step
                else:
                    text += current_char
                    pointer += 1
        # return the filtered string
        return text


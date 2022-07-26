from __future__ import annotations

import io
import os
from collections.abc import Iterable
from pathlib import Path
from token import INDENT, NEWLINE, NL
from tokenize import NAME, OP, STRING, TokenInfo, generate_tokens
from typing import TextIO


class ASort:
    @staticmethod
    def process_path(path: str) -> list[Path]:
        """
        given a path, recursively sort the __all__lists of all found python files
        if the path is a directory, otherwise, just sort the given file at the path

        :param path: the path to sort from
        :return: the files that were fixed
        """
        return process_path(path)


class Tokenizer:
    def __init__(self, input_stream: TextIO):
        self.input_stream = input_stream
        self.change_occured = False

    def __iter__(self):
        """
        process the given input_stream into a generator of sorted tokens

        :param input_stream: the stream of a python file to sort
        :return: true if the input_stream had a change, false if not
        """

        tokens = generate_tokens(self.input_stream.readline)
        curr_line = 1
        in_dund_all = False
        prev_token = TokenInfo(OP, "", (1, 0), (1, 0), "")
        dund_tokens = []

        for token in tokens:
            if token.start[0] > curr_line:
                curr_line = token.start[0]

            if in_dund_all:
                dund_tokens.append(token)
            else:
                yield token

            if (
                prev_token.string == "__all__"
                and prev_token.type == NAME
                and token.string == "="
                and token.type == OP
            ):
                in_dund_all = True

            if in_dund_all and token.string == "]":
                processed_dund_tokens = process_dund_tokens(dund_tokens)
                for pdt, dt in zip(processed_dund_tokens, dund_tokens):
                    if not _tokens_equal(dt, pdt):
                        self.change_occured = True
                    yield pdt
                in_dund_all = False
                dund_tokens = []

            prev_token = token


def process_path(path: str) -> list[Path]:
    """
    given a path, recursively sort the __all__ lists of all found python files

    :param path: the path to start the walk from
    """
    fixed_paths = []
    base_path = Path(path)
    if base_path.is_file():
        change = sort_file(base_path)
        if change:
            print(f"Fixing: {base_path}")
            fixed_paths.append(base_path)

    for root, _, files in os.walk(path):
        r = Path(root)
        for file in files:
            if file.endswith((".py", ".pyi")):
                filepath = r.joinpath(file)
                change = sort_file(filepath)
                if change:
                    print(f"Fixing: {filepath}")
                    fixed_paths.append(filepath)
    return fixed_paths


def sort_file(filepath: Path, output_stream: io.StringIO | None = None) -> bool:
    """
    given a file, sort it's __all__ lists

    :param filepath: the file to sort
    :param output_stream: the output stream to write to
    """
    out_stream = output_stream or io.StringIO()
    change_occured = False
    with open(file=filepath, mode="r", encoding="utf-8") as input_stream:
        tokenizer = Tokenizer(input_stream=input_stream)
        write_stream(tokenizer, output_stream=out_stream)
        change_occured = tokenizer.change_occured

    if output_stream:
        return change_occured

    with open(file=filepath, mode="w", encoding="utf-8") as output_file:
        output_file.writelines(out_stream.getvalue())
    out_stream.close()
    return change_occured


def process_dund_tokens(tokens: list[TokenInfo]) -> list[TokenInfo]:
    """
    sort the given list of tokens which represent an array assigned to a
    __all__ variable.

    :param tokens: the tokens to sort
    :return: the tokens sorted
    """

    tokens = list(tokens)
    if len(tokens) == 0:
        return tokens

    str_token_idxs = []
    str_token_line_nums = []
    str_token_lst = []
    spacing_before = [0]

    for idx, token in enumerate(tokens):
        if token.type == STRING:
            str_token_idxs.append(idx)
            str_token_line_nums.append(token.start[0])
            str_token_lst.append(token)
        if idx > 0:
            prev_token = tokens[idx - 1]
            same_line = token.start[0] == prev_token.end[0]
            if same_line:
                spacing_before.append(token.start[1] - prev_token.end[1])
            else:
                spacing_before.append(0)

    sorted_string_token_lst: list[TokenInfo] = sorted(
        str_token_lst, key=lambda x: x.string.replace("'", "").replace('"', "")
    )
    sorted_all_idxs: list[int] = sorted(str_token_idxs)
    sorted_all_line_nums: list[int] = sorted(str_token_line_nums)
    start_line = tokens[0].start[0]
    end_line = tokens[-1].start[0]
    same_line = start_line == end_line

    if same_line:
        for token, idx in zip(sorted_string_token_lst, sorted_all_idxs):
            existing_token = tokens[idx]
            token_len = token.end[1] - token.start[1]
            tokens[idx] = TokenInfo(
                token.type,
                token.string,
                (existing_token.start[0], existing_token.start[1]),
                (existing_token.end[0], existing_token.start[1] + token_len),
                token.line,
            )
    else:
        line_num_map: dict[int, int] = {
            token.start[0]: line_num
            for token, line_num in zip(sorted_string_token_lst, sorted_all_line_nums)
        }
        for idx, token in enumerate(tokens):
            line_num = line_num_map.setdefault(token.start[0], token.start[0])
            tokens[idx] = TokenInfo(
                token.type,
                token.string,
                (line_num, token.start[1]),
                (line_num, token.end[1]),
                token.line,
            )
        tokens = sorted(tokens, key=lambda x: (x.start[0], x.start[1]))

    # update start/end for whitespace
    prev_line_pos = tokens[0].start[1]
    prev_line = tokens[0].start[0]
    for idx, zipped in enumerate(zip(tokens, spacing_before)):
        token, l_spacing = zipped
        if token.start[0] != prev_line:
            prev_line = token.start[0]
            prev_line_pos = 0

        start_pos = prev_line_pos + l_spacing
        end_pos = start_pos + (token.end[1] - token.start[1])
        tokens[idx] = TokenInfo(
            token.type,
            token.string,
            (token.start[0], start_pos),
            (token.end[0], end_pos),
            token.line,
        )
        prev_line_pos = end_pos

    return tokens


def write_stream(processed_tokens: Iterable[TokenInfo], output_stream: TextIO) -> bool:
    """
    write the processed tokens to the output stream

    :param processed_tokens: the sorted tokens
    :param output_stream: the location the tokens are written to
    """
    prev_token: TokenInfo = TokenInfo(OP, "", (1, 0), (1, 0), "")

    for idx, token in enumerate(processed_tokens):
        if idx == 0:
            prev_token = token
            output_stream.write(token.string)
            continue

        same_line = prev_token.start[0] == token.end[0]
        if same_line:
            whitespace_len = token.start[1] - prev_token.end[1]
        else:
            whitespace_len = len(token.line) - len(token.line.lstrip())
            if token.string.isspace() or token.start[0] != token.end[0]:
                whitespace_len = 0

        output_stream.write(" " * whitespace_len)
        output_stream.write(token.string)
        prev_token = token

    return False


def _tokens_equal(base_token: TokenInfo, target_token: TokenInfo) -> bool:
    return (
        base_token.type == target_token.type
        and base_token.string == target_token.string
    )

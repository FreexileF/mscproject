from input import ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT, ARROW_UP, C_x_, C_, M_
MAX_UNICODE = 0x110000


def is_bound(cmd):
    return cmd in binding_table


def is_insertable(cmd):
    return cmd < MAX_UNICODE


binding_table = {
    C_('D'):            "show-version",
    C_x_(C_('S')):      "save-buffer",
    C_('W'):            "split-window",
    C_x_(C_('B')):      "list-buffer",
    C_x_(C_('C')):      "editor-exit",
    ARROW_DOWN:         "next-line",
    C_('N'):            "next-line",
    ARROW_UP:           "previous-line",
    C_('P'):            "prev-line",
    ARROW_RIGHT:        "right-char",
    C_('F'):            "right-char",
    ARROW_LEFT:         "left-char",
    C_('B'):            "left-char",
    C_x_('2'):          "split-window-vt",
    C_x_('3'):          "split-window-hz",
    C_x_("o"):          "other-window",
    C_x_(C_('F')):      "load-file",
    C_("A"):            'begin-of-line',
    C_("E"):            'end-of-line',
    C_x_("1"):          "merge-window",
    C_("H"):            "display-help-message",
    C_("K"):            "kill-to-eol",
    C_("V"):            "page-down",
    M_("V"):            "page-up",
    C_("S"):            "save-as"
    # C_("O"):            'open-line'
}

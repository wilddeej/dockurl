'''
Created on Dec 5, 2018

@author: deej Howard
@contact: wilddeej@gmail.com
'''
import argparse
import logging
import pyshorteners
from dockurl.dockurl import DockURL

def read_config_file(filename):
    '''
    Loads the YML configuration file.
    :param filename:
    '''
    from yaml import load
    error = ''
    to_return = {}
    try:
        with open(filename) as config_file:
            to_return = load(config_file)
    except FileNotFoundError as excpt:
        error = format(excpt)
        logging.warning("Couldn't load config file %s:\n%s\n" +
                        "Using default (empty) configuration instead", 
                        filename, error)
    return to_return

def determine_shorteners(all_shorteners, shorteners, full_config):
    '''
    Define the actual list of shorteners to use (either as specified, or
    from the full configuration list)
    :param all_shorteners:
    :param shorteners:
    :param full_config:
    '''

    shortener_list = []
    if 'config' in shorteners:
        # All configured shorteners - if there are any
        if 'shorteners' in full_config:
            logging.info("Determining shorteners from configuration")
            for item in full_config['shorteners']:
                # Is it a legal choice?
                if item['type'] in all_shorteners:
                    shortener_list.append(item['type'])
                else:
                    logging.error("%s is not a supported shortener - ignoring",
                                  item['type'])
        for item in shorteners:
            logging.info("Checking item '%s'...", item)
            if item != 'config':
                shortener_list.append(item)
        if not shortener_list:
            # Couldn't get the configured shorteners, so default to all
            logging.warning("Couldn't determine shorteners from " +
                            "configuration; defaulting to all supported")
            shortener_list = all_shorteners
    elif 'all' in shorteners:
        # All supported shorteners
        shortener_list = all_shorteners
    else:
        # Specified shorteners - assUme these are all legal
        shortener_list = shorteners

    return shortener_list

def configure_shorteners(all_shorteners, shorteners, full_config):
    '''
    Define the actual list of shorteners to use (either as specified, or
    from the full configuration list), and configure these with relevant
    data from the full configuration
    :param all_shorteners:
    :param shorteners:
    :param full_config:
    '''
    shortener_list = determine_shorteners(all_shorteners, shorteners, 
                                          full_config)
    shortener_configuration = {}

    if 'shorteners' in full_config:
        for item in full_config['shorteners']:
            if item['type'] in shortener_list:
                shortener_configuration[item['type']] = item['opts'] \
                    if 'opts' in item else {}
    for shortener in shortener_list:
        if shortener not in shortener_configuration:
            shortener_configuration[shortener] = {}

    return shortener_list, shortener_configuration

def main():
    '''Entry point if called as an executable'''

    
    all_shorteners = pyshorteners.Shortener().available_shorteners
    # Parse input args
    parser = argparse.ArgumentParser(
        prog='dockurl',
        description='Execute URL shortening functions')
    # TODO: Option to output in JSON format?
    # TODO: Option to list out all valid shorteners and exit (no URL needed)
    # Verbosity level
    parser.add_argument('-v', '--verbose', action='count')
    # Optional config file (use default otherwise)
    parser.add_argument('-c', '--config', default='dockurl.yml',
                        help='configuration file name')
    # Optional action (use default otherwise)
    parser.add_argument('-a', '--action', default='shorten',
                        choices=['shorten', 'expand', 'click-count'],
                        help='action to execute')
    # Optional shortener type (action attempted against default otherwise)
    # TODO: Multiple shorteners only valid for 'shorten' option, all others
    #       can accept only one shortener
    parser.add_argument('-s', '--shortener', nargs='+', default=['config'],
                        choices=['all', 'config'] + all_shorteners,
                        help='shortener(s) to use')
    # MUST be passed one or more URLs
    parser.add_argument('url', nargs='+',
                        help='URL(s) upon which to act')
    args = parser.parse_args()

    # Initialize DockURL, which also sets logging config
    dockurl = DockURL(args.verbose)

    # Read in config, or default to empty config
    full_config = read_config_file(args.config)

    short_list, short_config = configure_shorteners(all_shorteners,
                                                    args.shortener,
                                                    full_config)

    logging.info("Executing %s action on URL%s:\n\t%s\nusing %s shortener%s",
                 args.action, 's' if len(args.url) > 1 else '',
                 "\n\t".join(args.url), ", ".join(short_list),
                 's' if len(short_list) > 1 else '')
    dockurl.set_config(short_config)
    dockurl.set_action(args.action)
    dockurl.set_shorteners(short_list)
    dockurl.set_urls(args.url)
    dockurl.run()

if __name__ == '__main__':
    main()

#!/usr/bin/python3
import argparse
import json
import yaml


class S3ClientCfg:
    __pillar_data_options = {}
    __cfg_path = ""


    def __init__(self, arg_parser, cfg_path):
        if not arg_parser:
            raise Exception("Class cannot be initialized without an argparse object")

        self.__cfg_path = cfg_path
        self.__setup_args(arg_parser)
        self.__load_defaults()


    def __setup_args(self, arg_parser):
        # TODO - validate for accidental override
        arg_parser.add_argument(
            '--s3client-file',
            dest = 's3client_file',
            action="store",
            help='Yaml file with s3client configs')

        arg_parser.add_argument(
            '--show-s3client-file-format',
            dest = 'show_s3client_file_format',
            action="store_true",
            help='Display Yaml file format for s3client configs')


    def __load_defaults(self):
        with open(self.__cfg_path, 'r') as fd:
            self.__pillar_data_options = yaml.load(fd, Loader=yaml.FullLoader)
        # print(json.dumps(self.__pillar_data_options, indent = 4))
        # TODO validations for configs.


    def process_inputs(self, arg_parser):
        program_args = arg_parser.parse_args()

        if program_args.show_s3client_file_format:
            print(self.__pillar_data_options)
            return False
        elif program_args.s3client_file:
            # Load s3server file and merge options.
            new_options = {}
            with open(program_args.file, 'r') as fd:
                new_options = yaml.load(fd, Loader=yaml.FullLoader)
                self.__pillar_data_options.update(new_options)
        elif program_args.interactive:
            input_msg = ("S3Server FQDN [{0}]: ".format(self.__pillar_data_options["s3client"]["s3server"]["ip"]))
            self.__pillar_data_options["s3client"]["s3server"]["fqdn"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["s3server"]["fqdn"]
            input_msg = ("S3Server IP [{0}]: ".format(self.__pillar_data_options["s3client"]["s3server"]["ip"]))
            self.__pillar_data_options["s3client"]["s3server"]["ip"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["s3server"]["ip"]

            input_msg = ("S3 Access Key: ")
            self.__pillar_data_options["s3client"]["access_key"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["access_key"]
            input_msg = ("S3 Secret Key: ")
            self.__pillar_data_options["s3client"]["secret_key"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["secret_key"]
            input_msg = ("Region [{0}]: ".format(self.__pillar_data_options["s3client"]["region"]))
            self.__pillar_data_options["s3client"]["region"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["region"]
            input_msg = ("Output format [{0}]: ".format(self.__pillar_data_options["s3client"]["output"]))
            self.__pillar_data_options["s3client"]["output"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["output"]
            input_msg = ("S3 Endpoint [{0}]: ".format(self.__pillar_data_options["s3client"]["s3endpoint"]))
            self.__pillar_data_options["s3client"]["s3endpoint"] = input(
                input_msg) or self.__pillar_data_options["s3client"]["s3endpoint"]
            # print(json.dumps(self.__pillar_data_options, indent = 4))
        else:
            # print("ERROR: No usable inputs provided.")
            return False


    def save(self):
        with open(self.__cfg_path, 'w') as fd:
            yaml.dump(self.__pillar_data_options, fd, default_flow_style = False)

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 2022-06-29
Sometimes market stream can hang if you start it before start trading session.
To avoid this issue:
- Added awaiting to start market stream if the tool has been started before start trading session.  
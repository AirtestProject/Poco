# coding=utf-8

"""
**The brief introduction**:

This package (:py:mod:`poco.sdk.interfaces`) defines the main standards for communication interfaces between poco and
poco-sdk. If poco-sdk is integrated with an app running on another host or in different language, then poco-sdk is
called `remote runtime`. The implementation of these interfaces can be done either remotely or locally depending on
your own choice. If it is done locally, refer to :py:mod:`poco.freezeui` for more information.

Poco needs to communicate with the app runtime under the convention of interfaces described below and these interfaces
must be properly implemented. Any object implementing the same interface is replaceable and the communication protocol
or transport layer has no limitation. Furthermore, in many cases the communication can be customized that one part of
interfaces can use HTTP protocol and other can use TCP.

"""

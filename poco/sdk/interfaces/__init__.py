# coding=utf-8

"""
package brief:

This package (:py:mod:`poco.sdk.interfaces`) defines the main communication interfaces that standardize between poco and 
poco-sdk. When poco-sdk is integrated with an app running on another machine or in different language, poco-sdk is 
called remote runtime. The implementations of these interfaces can be remotely or locally, depending on you. If locally, 
please checkout :py:mod:`poco.freezeui` to get more information.

Poco needs to communicated with app's runtime under the convention of these interfaces. These interfaces should be 
implemented properly. Any object implemented the same interface is replaceable. The communication protocol or transport 
layer is not limited. Thus in many cases, it is customizable that part of the interface can be implemented using HTTP 
and another part with TCP.
"""

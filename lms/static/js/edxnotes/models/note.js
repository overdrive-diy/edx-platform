;(function (define, gettext, interpolate, undefined) {
    'use strict';
    define(['jquery', 'backbone'], function ($, Backbone) {
        var NoteModel = Backbone.Model.extend({
            defaults: {
                'id': null,
                'created': null,
                'updated': null,
                'user': null,
                'usage_id': null,
                'course_id': null,
                'text': null,
                'quote': null,
                'unit': {
                    'display_name': null,
                    'url': null
                },
                'ranges': []
            },

            timeFormat: 'hh:mmtt', // For example: 12:59PM
            dateFormat: 'MMMM dd, yyyy', // For example: November 11, 2014

            parse: function (attributes) {
                if (attributes.updated) {
                    attributes.updated = this.getUTCDate(attributes.updated);
                }
                if (attributes.created) {
                    attributes.created = this.getUTCDate(attributes.created);
                }
                return attributes;
            },

            getUTCDate: function (dateString) {
                var date = new Date(dateString);
                return Date.UTC(
                    date.getFullYear(), date.getMonth(), date.getDay(),
                    date.getHours(), date.getMinutes(), date.getSeconds(),
                    date.getMilliseconds()
                );
            },

            getDateTime: function (utcDate) {
                var datetime = new Date(utcDate),
                    datetimeString = gettext('%(date)s at %(time)s');

                return interpolate(datetimeString, {
                    date: datetime.toString(this.dateFormat),
                    time: datetime.toString(this.timeFormat)
                }, true);
            },

            toJSON: function () {
                return $.extend(true, {}, this.attributes, {
                    created: this.getDateTime(this.get('created')),
                    updated: this.getDateTime(this.get('updated'))
                });
            }
        });

        return NoteModel;
    });
}).call(this, define || RequireJS.define, gettext, interpolate);
